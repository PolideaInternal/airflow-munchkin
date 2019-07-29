# -*- coding: utf-8 -*-
import logging
from typing import List, Dict

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    MethodBlock,
    CodeBlock,
    FileBlock,
    ParameterBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import ActionInfo, ClientInfo
from airflow_munchkin.integration import Integration


def generate_get_conn_method_block(integration: Integration) -> MethodBlock:
    client_type = TypeBrick(integration.client_path)
    method_block = MethodBlock(
        name="get_conn",
        desc=[
            f"Retrieves client library object that allow access to {integration.service_name} service."
        ],
        args={},
        return_kind=client_type,
        return_desc=[f"{integration.service_name} client object."],
        code_blocks=[
            CodeBlock(
                template_name="get_conn_body.py.tpl",
                template_params={"client": client_type},
            )
        ],
    )
    return method_block


def generate_method_block(action_info: ActionInfo) -> MethodBlock:
    blocks: List[CodeBlock] = []
    args: Dict[str, ParameterBlock] = {}
    for arg in action_info.args.values():
        kind = arg.kind
        default_value = None
        if kind and kind.is_optional:
            kind = kind.indexes[0]
            default_value = "None"
        args[arg.name] = ParameterBlock(
            name=arg.name, kind=kind, desc=arg.desc, default_value=default_value
        )
    method_block = MethodBlock(
        name=action_info.name,
        desc=action_info.desc,
        args=args,
        return_kind=action_info.return_kind,
        return_desc=action_info.return_desc,
        code_blocks=blocks,
    )
    blocks.append(CodeBlock(template_name="client_init.py.tpl", template_params=dict()))
    blocks.append(
        CodeBlock(
            template_name="client_call.py.tpl",
            template_params=dict(
                var_name="result" if action_info.return_desc else None,
                name=action_info.name,
                call_params={arg: arg for arg in action_info.args},
            ),
        )
    )
    if action_info.return_desc:
        blocks.append(
            CodeBlock(
                template_name="return.py.tpl",
                template_params=dict(
                    var_name="result" if action_info.return_desc else None
                ),
            )
        )
    return method_block


def generate_class_block(
    client_info: ClientInfo, integration: Integration
) -> ClassBlock:
    ctor_method = generate_ctor_method(client_info)
    get_conn_method = generate_get_conn_method_block(integration)
    hook_methods = [ctor_method, get_conn_method]

    for info in client_info.action_methods.values():
        method_block = generate_method_block(info)
        hook_methods.append(method_block)
    class_block = ClassBlock(
        name=f"{integration.class_prefix}Hook",
        extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
        methods_blocks=hook_methods,
    )
    return class_block


def generate_ctor_method(client_info):
    ctor_method = MethodBlock(
        name="__init__",
        desc=client_info.ctor_method.desc,
        args=client_info.ctor_method.args,
        return_kind=client_info.ctor_method.return_kind,
        return_desc=client_info.ctor_method.return_desc,
        code_blocks=[],
    )
    return ctor_method


def create_file_block(client_info: ClientInfo, integration: Integration) -> FileBlock:
    logging.info("Start creating hook block")
    class_block = generate_class_block(client_info, integration)
    file_block: FileBlock = FileBlock(
        file_name=f"{integration.file_prefix}_hook.py", class_blocks=[class_block]
    )
    imports_statement_gather.update_imports_statements(file_block)
    logging.info("Finished creating hook block")
    return file_block
