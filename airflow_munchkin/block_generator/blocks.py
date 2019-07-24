# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Dict, Any, Set, Optional

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import ParameterInfo


class CodeBlock(NamedTuple):
    template_name: str
    template_params: Dict[str, Any]


class MethodBlock(NamedTuple):
    name: str
    desc: Optional[List[str]]
    args: Dict[str, ParameterInfo]
    return_kind: Optional[TypeBrick]
    return_desc: Optional[List[str]]
    code_blocks: List[CodeBlock]


class ClassBlock(NamedTuple):
    name: str
    extend_class: str
    methods_blocks: List[MethodBlock]


class FileBlock(NamedTuple):
    file_name: str
    class_blocks: List[ClassBlock]
    import_statement: Set[str] = {
        "typing.Union",
        "typing.Optional",
        "typing.Sequence",
        "typing.Tuple",
        "typing.Dict",
        "airflow.AirflowException",
        "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
        "google.api_core.retry.Retry",
        "google.cloud.redis_v1beta1.CloudRedisClient",
    }
