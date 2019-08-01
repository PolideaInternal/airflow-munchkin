# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    MethodBlock,
    CodeBlock,
    FileBlock,
    ParameterBlock,
)
from airflow_munchkin.client_parser import ClientInfo
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import ActionInfo
from airflow_munchkin.integration import Integration


def generate_setup_method_block(class_path: str, init_new: str) -> MethodBlock:
    method_block = MethodBlock(
        name="setUp",
        desc=None,
        args={},
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=[
            CodeBlock(
                template_name="setup_mock.py.tpl",
                template_params={"class_path": class_path, "new": init_new},
            )
        ],
    )
    return method_block


def generate_test_method_for_client_call(
    action_info: ActionInfo,
    hook_method_block: MethodBlock,
    hook_class_path: str,
    project_id_value: str,
):
    code_blocks = [
        CodeBlock(
            template_name="method_call.py.tpl",
            template_params={
                "target": f"self.hook.{hook_method_block.name}",
                "call_params": {
                    arg_name: f"TEST_{arg_name.upper()}"
                    for arg_name in hook_method_block.args.keys()
                },
            },
        ),
        CodeBlock(
            template_name="method_call.py.tpl",
            template_params={
                "target": f"mock_get_conn.{action_info.name}.assert_called_once_with",
                "call_params": {
                    arg_name: f"TEST_{arg_name.upper()}"
                    if arg_name != "project_id"
                    else project_id_value
                    for arg_name in action_info.args.keys()
                },
            },
        ),
    ]
    method_block = MethodBlock(
        name=f"test_{hook_method_block.name}",
        desc=None,
        args={"mock_get_conn": ParameterBlock("mock_get_conn")},
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=code_blocks,
        decorator_blocks=[
            CodeBlock(
                template_name="decorator_mock_get_conn.py.tpl",
                template_params={"class_path": hook_class_path},
            )
        ],
    )
    return method_block


def generate_test_method_for_call_without_project_id(
    hook_class_path: str, hook_method_block: MethodBlock
) -> MethodBlock:
    code_blocks = [
        CodeBlock(
            template_name="method_call_assert_raises.py.tpl",
            template_params={
                "target": f"self.hook.{hook_method_block.name}",
                "call_params": {
                    a: f"TEST_{a.upper()}" if a != "project_id" else "None"
                    for a in hook_method_block.args.keys()
                },
            },
        )
    ]
    method_block = MethodBlock(
        name=f"test_{hook_method_block.name}_without_project_id",
        desc=None,
        args={"mock_get_conn": ParameterBlock("mock_get_conn")},
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=code_blocks,
        decorator_blocks=[
            CodeBlock(
                template_name="decorator_mock_get_conn.py.tpl",
                template_params={"class_path": hook_class_path},
            )
        ],
    )
    return method_block


def generate_class_block_without_default_project_id(
    hook_class_path: str,
    hook_class: ClassBlock,
    client_info: ClientInfo,
    integration: Integration,
) -> ClassBlock:
    hook_methods = []
    hook_methods.append(
        generate_setup_method_block(
            hook_class_path, "mock_base_gcp_hook_no_default_project_id"
        )
    )
    for name in client_info.action_methods.keys():
        action_info = client_info.action_methods[name]
        hook_method_block = next(m for m in hook_class.methods_blocks if m.name == name)
        hook_methods.append(
            generate_test_method_for_client_call(
                action_info, hook_method_block, hook_class_path, "TEST_PROJECT_ID"
            )
        )
        if "project_id" in hook_method_block.args:
            hook_methods.append(
                generate_test_method_for_call_without_project_id(
                    hook_class_path, hook_method_block
                )
            )
    class_block = ClassBlock(
        name=f"Test{integration.class_prefix}WithoutDefaultProjectIdHook",
        extend_class="unittest.TestCase",
        methods_blocks=hook_methods,
    )
    return class_block


def generate_class_block_with_default_project_id(
    hook_class_path: str,
    hook_class: ClassBlock,
    client_info: ClientInfo,
    integration: Integration,
) -> ClassBlock:
    hook_methods = []
    hook_methods.append(
        generate_setup_method_block(
            hook_class_path, "mock_base_gcp_hook_default_project_id"
        )
    )
    for name in client_info.action_methods.keys():
        action_info = client_info.action_methods[name]
        hook_method_block = next(m for m in hook_class.methods_blocks if m.name == name)
        hook_methods.append(
            generate_test_method_for_client_call(
                action_info,
                hook_method_block,
                hook_class_path,
                "GCP_PROJECT_ID_HOOK_UNIT_TEST",
            )
        )
    class_block = ClassBlock(
        name=f"Test{integration.class_prefix}WithDefaultProjectIdHook",
        extend_class="unittest.TestCase",
        methods_blocks=hook_methods,
    )
    return class_block


def create_file_block(
    hook_file_block: FileBlock, client_info: ClientInfo, integration: Integration
) -> FileBlock:
    logging.info("Start creating hook test file block")
    hook_module_name, _ = hook_file_block.file_name.rsplit(".", 2)  # drop ".py"
    hook_class = hook_file_block.class_blocks[0]
    hook_class_path = f"airflow.contrib.hooks.{hook_module_name}.{hook_class.name}"

    class_block_with_default_project_id = generate_class_block_with_default_project_id(
        hook_class_path, hook_class, client_info, integration
    )
    class_block_without_default_project_id = generate_class_block_without_default_project_id(
        hook_class_path, hook_class, client_info, integration
    )

    file_block: FileBlock = FileBlock(
        file_name=f"test_{integration.file_prefix}_hook.py",
        class_blocks=[
            class_block_with_default_project_id,
            class_block_without_default_project_id,
        ],
    )
    imports_statement_gather.update_imports_statements(file_block)
    file_block.import_statement.add(hook_class_path)
    logging.info("Finished creating hook test file block")
    return file_block
