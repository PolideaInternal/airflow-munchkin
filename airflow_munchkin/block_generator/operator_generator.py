# -*- coding: utf-8 -*-
import logging
from typing import List

from airflow_munchkin import utils
from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import (
    FileBlock,
    ClassBlock,
    MethodBlock,
    ParameterBlock,
    CodeBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.integration import Integration


def create_operator_class_block(
    hook_class_name: str, hook_method: MethodBlock, integration: Integration
) -> ClassBlock:

    init_args = {
        **dict(hook_method.args.items()),
        "gcp_conn_id": ParameterBlock(
            "gcp_conn_id", kind=TypeBrick("str"), default_value="'google_cloud_default'"
        ),
    }
    super_args = {
        "*args": ParameterBlock("*args"),
        "**kwargs": ParameterBlock("**kwargs"),
    }

    ctor_method_block = MethodBlock(
        name="__init__",
        desc=hook_method.desc,
        args={**init_args, **super_args},
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=[
            CodeBlock(
                template_name="super_call.py.tpl",
                template_params={"args": list(super_args.keys()), "kwargs": {}},
            ),
            *(
                CodeBlock(
                    template_name="set_field.py.tpl",
                    template_params={
                        "field_name": arg_name,
                        "field_value": arg_name,
                        "field_type": None,
                    },
                )
                for arg_name in init_args.keys()
            ),
        ],
        decorator_blocks=[
            CodeBlock(
                template_name="decorator_apply_defaults.py.tpl", template_params={}
            )
        ],
    )
    execute_method_block = MethodBlock(
        name="execute",
        desc=None,
        args={"context": ParameterBlock("context", TypeBrick("Dict"))},
        return_kind=None,
        return_desc=None,
        code_blocks=[
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "var_name": "hook",
                    "target": hook_class_name,
                    "call_params": {"gcp_conn_id": "self.gcp_conn_id"},
                },
            ),
            CodeBlock(
                template_name="method_call.py.tpl",
                template_params={
                    "target": f"hook.{hook_method.name}",
                    "call_params": {
                        arg_name: f"self.{arg_name}" for arg_name in hook_method.args
                    },
                },
            ),
        ],
        decorator_blocks=[
            CodeBlock(
                template_name="decorator_apply_defaults.py.tpl", template_params={}
            )
        ],
    )
    return ClassBlock(
        name=f"{integration.class_prefix}{utils.to_camel_case(hook_method.name)}Operator",
        extend_class="airflow.models.BaseOperator",
        methods_blocks=[ctor_method_block, execute_method_block],
    )


def create_operator_class_blocks(
    hook_class: ClassBlock, integration: Integration
) -> List[ClassBlock]:
    return [
        create_operator_class_block(
            hook_class_name=hook_class.name, hook_method=m, integration=integration
        )
        for m in hook_class.methods_blocks
        if m.name != "__init__" and m.name != "get_conn"
    ]


def create_file_block(
    integration: Integration, hook_file_block: FileBlock
) -> FileBlock:
    logging.info("Start creating operators file block")
    hook_module_name, _ = hook_file_block.file_name.rsplit(".", 2)  # drop ".py"
    hook_class = hook_file_block.class_blocks[0]
    hook_class_path = f"airflow.contrib.hooks.{hook_module_name}.{hook_class.name}"

    operator_class_blocks = create_operator_class_blocks(hook_class, integration)

    file_block: FileBlock = FileBlock(
        file_name=f"{integration.file_prefix}_operator.py",
        class_blocks=operator_class_blocks,
    )

    imports_statement_gather.update_imports_statements(file_block)
    file_block.import_statement.add(hook_class_path)
    logging.info("Finished creating operators file block")
    return file_block
