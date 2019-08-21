# -*- coding: utf-8 -*-
from typing import Any, Dict, List, NamedTuple, Optional, Set

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


DEFAULT_IMPORTS = (
    "typing.Union",
    "typing.Optional",
    "typing.Sequence",
    "typing.Tuple",
    "typing.Dict",
    "airflow.AirflowException",
    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
    "google.api_core.retry.Retry",
    "google.cloud.redis_v1beta1.CloudRedisClient",
    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
    "tests.contrib.utils.base_gcp_mock.GCP_PROJECT_ID_HOOK_UNIT_TEST",
    "unittest.TestCase",
    "unittest.mock",
    "airflow.utils.decorators.apply_defaults",
)


class CodeBlock(NamedTuple):
    template_name: str
    template_params: Dict[str, Any]


class ParameterBlock(NamedTuple):
    name: str
    kind: Optional[TypeBrick] = None
    desc: Optional[List[str]] = None
    default_value: Optional[str] = None


class MethodBlock(NamedTuple):
    name: str
    desc: Optional[List[str]]
    args: Dict[str, ParameterBlock]
    return_kind: Optional[TypeBrick]
    return_desc: Optional[List[str]]
    code_blocks: List[CodeBlock]
    decorator_blocks: List[CodeBlock] = []


class ClassBlock(NamedTuple):
    name: str
    extend_class: str
    methods_blocks: List[MethodBlock]


class Constant(NamedTuple):
    name: str
    value: str
    kind: Optional[TypeBrick] = None


class FileBlock:
    def __init__(
        self,
        file_name: str,
        class_blocks: List[ClassBlock],
        import_statement: Set[str] = None,
        constants: List[Constant] = None,
    ):
        self.file_name = file_name
        self.class_blocks = class_blocks
        self.import_statement = import_statement or {*DEFAULT_IMPORTS}
        self.constants = constants or []

    def __str__(self) -> str:
        return (
            f"FileBlock(file_name={repr(self.file_name)}, class_blocks={self.class_blocks}, "
            f"import_statement={self.import_statement}, constants={repr(self.constants)})"
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(
            (self.file_name, self.class_blocks, self.import_statement, self.constants)
        )
