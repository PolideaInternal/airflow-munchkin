# -*- coding: utf-8 -*-
import logging
import re
from typing import List, Dict, Tuple

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    MethodBlock,
    CodeBlock,
    FileBlock,
    ParameterBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import (
    ActionInfo,
    ClientInfo,
    PathInfo,
    ParameterInfo,
)
from airflow_munchkin.exceptions import GeneratorException
from airflow_munchkin.integration import Integration


def generate_ctor_method_block(
    client_info: ClientInfo, integration: Integration
) -> MethodBlock:
    args = {
        "gcp_conn_id": ParameterBlock(name="gcp_conn_id", kind=TypeBrick("str")),
        "delegate_to": ParameterBlock(name="delegate_to", kind=TypeBrick("str")),
    }
    method_block = MethodBlock(
        name="__init__",
        desc=client_info.ctor_method.desc,
        args=args,
        return_kind=TypeBrick("None"),
        return_desc=None,
        code_blocks=[
            CodeBlock(
                template_name="super_call.py.tpl",
                template_params={"args": list(args.keys()), "kwargs": {}},
            ),
            CodeBlock(
                template_name="set_field.py.tpl",
                template_params={
                    "field_name": "_client",
                    "field_type": integration.client_type_brick,
                    "field_value": "None",
                },
            ),
        ],
    )
    return method_block


def generate_get_conn_method_block(integration: Integration) -> MethodBlock:
    method_block = MethodBlock(
        name="get_conn",
        desc=[
            f"Retrieves client library object that allow access to {integration.service_name} service."
        ],
        args={},
        return_kind=integration.client_type_brick,
        return_desc=[f"{integration.service_name} client object."],
        code_blocks=[
            CodeBlock(
                template_name="get_conn_body.py.tpl",
                template_params={"client": integration.client_type_brick},
            )
        ],
    )
    return method_block


PATH_REGEXP = re.compile(r"``(?P<path>(?:[a-z{}_ ]+\/[a-z{}_ ]+)+)``")
PATH_SEGMENT_REGEXP = re.compile(r"{([a-z_]+)}")


def find_matching_path_info(path: str, path_infos: Dict[str, PathInfo]) -> PathInfo:
    segments = (m.group(1) for m in PATH_SEGMENT_REGEXP.finditer(path))
    arguments = [a.partition("_id")[0] for a in segments]

    for path_info in path_infos.values():
        if path_info.args == arguments:
            return path_info
    raise GeneratorException(
        f"The path could not be determined. Current path: '${path}'"
    )


def convert_path_parameter_block_to_individual_parameters(
    path_parameter: ParameterInfo,
    path_infos: Dict[str, PathInfo],
    integration: Integration,
) -> Tuple[Dict[str, ParameterBlock], Dict[str, ParameterBlock], CodeBlock]:
    match = PATH_REGEXP.search("\n".join(path_parameter.desc))
    if not match:
        raise GeneratorException("")

    path = match["path"]
    path_info = find_matching_path_info(path, path_infos=path_infos)
    optional_parameters: Dict[str, ParameterBlock] = {}
    required_parameters: Dict[str, ParameterBlock] = {}
    call_args = []

    for name in path_info.args:
        if name == "project":
            optional_parameters["project_id"] = ParameterBlock(
                name="project_id",
                kind=TypeBrick("str"),
                desc=["TODO: Fill description"],
                default_value="None",
            )
            call_args.append("project_id")
        else:
            required_parameters[name] = ParameterBlock(
                name=name, kind=TypeBrick("str"), desc=["TODO: Fill description"]
            )
            call_args.append(name)
    code_block = CodeBlock(
        template_name="call_path.py.tpl",
        template_params={
            "var_name": path_parameter.name,
            "fn_name": path_info.name,
            "args": call_args,
            "client": integration.client_type_brick,
        },
    )
    return required_parameters, optional_parameters, code_block


def generate_method_block(
    action_info: ActionInfo, path_infos: Dict[str, PathInfo], integration: Integration
) -> MethodBlock:
    blocks: List[CodeBlock] = []
    blocks.append(CodeBlock(template_name="client_init.py.tpl", template_params=dict()))

    optional_parameters: Dict[str, ParameterBlock] = {}
    required_parameters: Dict[str, ParameterBlock] = {}
    for arg in action_info.args.values():
        if arg.name == "parent" or arg.name == "name":
            new_req_params, new_opt_params, code = convert_path_parameter_block_to_individual_parameters(
                path_parameter=arg, path_infos=path_infos, integration=integration
            )
            required_parameters.update(new_req_params)
            optional_parameters.update(new_opt_params)
            blocks.append(code)
            continue
        kind = arg.kind
        default_value = None
        if kind and kind.is_optional:
            kind = kind.indexes[0]
            default_value = "None"
            optional_parameters[arg.name] = ParameterBlock(
                name=arg.name, kind=kind, desc=arg.desc, default_value=default_value
            )
        else:
            required_parameters[arg.name] = ParameterBlock(
                name=arg.name, kind=kind, desc=arg.desc, default_value=default_value
            )

    method_block = MethodBlock(
        name=action_info.name,
        desc=action_info.desc,
        args={**required_parameters, **optional_parameters},
        return_kind=action_info.return_kind,
        return_desc=action_info.return_desc,
        code_blocks=blocks,
    )
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
    ctor_method = generate_ctor_method_block(client_info, integration)
    get_conn_method = generate_get_conn_method_block(integration)
    hook_methods = [ctor_method, get_conn_method]

    for info in client_info.action_methods.values():
        method_block = generate_method_block(
            info, path_infos=client_info.path_methods, integration=integration
        )
        hook_methods.append(method_block)
    class_block = ClassBlock(
        name=f"{integration.class_prefix}Hook",
        extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
        methods_blocks=hook_methods,
    )
    return class_block


def create_file_block(client_info: ClientInfo, integration: Integration) -> FileBlock:
    logging.info("Start creating hook block")
    class_block = generate_class_block(client_info, integration)
    file_block: FileBlock = FileBlock(
        file_name=f"{integration.file_prefix}_hook.py", class_blocks=[class_block]
    )
    imports_statement_gather.update_imports_statements(file_block)
    logging.info("Finished creating hook block")
    return file_block
