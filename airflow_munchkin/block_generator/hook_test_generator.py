# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    MethodBlock,
    CodeBlock,
    FileBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
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


def generate_class_block_without_default_project_id(
    hook_class_path: str, integration: Integration
) -> ClassBlock:

    hook_methods = []
    hook_methods.append(
        generate_setup_method_block(
            hook_class_path, "mock_base_gcp_hook_no_default_project_id"
        )
    )
    class_block = ClassBlock(
        name=f"Test{integration.class_prefix}Hook",
        extend_class="unittest.TestCase",
        methods_blocks=hook_methods,
    )
    return class_block


def create_file_block(
    hook_file_block: FileBlock, integration: Integration
) -> FileBlock:
    logging.info("Start creating hook test file block")
    hook_module_name, _ = hook_file_block.file_name.rsplit(".", 2)  # drop ".py"
    hook_class = hook_file_block.class_blocks[0]
    hook_class_path = f"airflow.contrib.hooks.{hook_module_name}.{hook_class.name}"

    class_block_without_default_project_id = generate_class_block_without_default_project_id(
        hook_class_path, integration
    )
    file_block: FileBlock = FileBlock(
        file_name=f"test_{integration.file_prefix}_hook.py",
        class_blocks=[class_block_without_default_project_id],
    )
    imports_statement_gather.update_imports_statements(file_block)
    file_block.import_statement.add(hook_class_path)
    logging.info("Finished creating hook test file block")
    return file_block
