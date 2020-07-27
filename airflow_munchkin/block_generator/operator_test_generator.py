# -*- coding: utf-8 -*-
import logging
from typing import List

from airflow_munchkin.block_generator import (
    imports_statement_gather,
    constant_generator,
)
from airflow_munchkin.block_generator.blocks import (
    FileBlock,
    ClassBlock,
    MethodBlock,
    ParameterBlock,
    CodeBlock,
    Constant,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.exceptions import GeneratorException
from airflow_munchkin.integration import Integration


def find_client_call_method_name(operator_class: ClassBlock) -> str:
    for method_block in operator_class.methods_blocks:
        if method_block.name != "execute":
            continue
        method_call = next(
            code_block
            for code_block in method_block.code_blocks
            if code_block.template_params["target"].startswith("hook.")
        )
        method_name: str
        _, _, method_name = method_call.template_params["target"].partition(".")
        return method_name
    raise GeneratorException("The hook method could not be determined.")


def create_assert_call_method_block(
    operator_module_path: str, hook_class_name: str, operator_class_block: ClassBlock
) -> MethodBlock:
    ctor_method = next(
        m for m in operator_class_block.methods_blocks if m.name == "__init__"
    )
    ctor_args = [a for a in ctor_method.args.keys() if a not in ("*args", "**kwargs")]

    method_name = find_client_call_method_name(operator_class_block)

    return MethodBlock(
        name="test_assert_valid_hook_call",
        desc=None,
        args={"mock_hook": ParameterBlock("mock_hook")},
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=[
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "var_name": "task",
                    "target": operator_class_block.name,
                    "call_params": {a: f"TEST_{a.upper()}" for a in ctor_args},
                },
            ),
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "target": "task.execute",
                    "call_params": {"context": "mock.MagicMock()"},
                },
            ),
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "target": "mock_hook.assert_called_once_with",
                    "call_params": {"gcp_conn_id": "TEST_GCP_CONN_ID"},
                },
            ),
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "target": f"mock_hook.return_value.{method_name}.assert_called_once_with",
                    "call_params": {
                        a: f"TEST_{a.upper()}" for a in ctor_args if a != "gcp_conn_id"
                    },
                },
            ),
        ],
        decorator_blocks=[
            CodeBlock(
                "decorator_mock_hook.py.tpl",
                template_params={
                    "class_path": f"{operator_module_path}.{hook_class_name}"
                },
            )
        ],
    )


def create_operator_test_class_blocks(
    operator_module_path: str, hook_class_name: str, operator_class: ClassBlock
) -> ClassBlock:
    return ClassBlock(
        name=f"Test{operator_class.name}",
        extend_class="unittest.TestCase",
        methods_blocks=[
            create_assert_call_method_block(
                operator_module_path, hook_class_name, operator_class
            )
        ],
    )


def create_constants(operator_class_blocks: List[ClassBlock]) -> List[Constant]:
    all_methods = (m for op in operator_class_blocks for m in op.methods_blocks)
    ctors_method = (m for m in all_methods if m.name == "__init__")
    unique_constant = {
        a.name: a.kind
        for m in ctors_method
        for a in m.args.values()
        if a.name not in ("*args", "**kwargs")
    }
    constants = constant_generator.generate_constant_list(unique_constant)

    return constants


def create_file_block(
    operator_file_block: FileBlock, hook_file_block: FileBlock, integration: Integration
) -> FileBlock:
    logging.info("Start creating operators test file block")
    operator_module_name, _ = operator_file_block.file_name.rsplit(".", 2)  # drop ".py"
    operator_module_path = f"airflow.contrib.operator.{operator_module_name}"
    hook_class_name = hook_file_block.class_blocks[0].name

    test_class_blocks = [
        create_operator_test_class_blocks(
            operator_module_path, hook_class_name, operator_class_block
        )
        for operator_class_block in operator_file_block.class_blocks
    ]
    constants = create_constants(operator_file_block.class_blocks)
    file_block: FileBlock = FileBlock(
        file_name=f"test_{integration.file_prefix}_operator.py",
        class_blocks=test_class_blocks,
        constants=constants,
    )

    imports_statement_gather.update_imports_statements(file_block)
    for operator_class_block in operator_file_block.class_blocks:
        operator_class_path = f"{operator_module_path}.{operator_class_block.name}"
        file_block.import_statement.add(operator_class_path)
    logging.info("Finished creating operators test file block")
    return file_block
