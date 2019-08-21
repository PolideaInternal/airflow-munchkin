# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Optional, Any
from airflow_munchkin.discovery_parser.utils import map_type, camel_to_snake


class Parameter(NamedTuple):
    name: str
    kind: Optional[str]
    desc: List[str]
    required: bool
    default: Optional[Any] = None

    """
    :param name: orginal name of the parameter
    :param kind: type of the parameter
    :param desc: description of the parameter
    :param required: True if parameter is required for a method
    :param default: default value of the parameter
    """

    @classmethod
    def from_dict(cls, param_name, parameter_info: dict):
        """
        Creates `Parameter` from dictionary in form of
        ```
        {
            "type": "string",
            "description": "ID of the report request being polled.",
            "required": True,
            "location": "path",
        }
        ```

        :param param_name: name of the parameter
        :param parameter_info: dictionary with information about the parameter
        """
        name = param_name
        desc = [parameter_info["description"]]
        required = parameter_info.get("required", False)
        kind = map_type(parameter_info["type"])
        kind = "Optional[{}]".format(kind) if not required else kind
        return cls(name=name, kind=kind, desc=desc, required=required)

    @property
    def pythonic_name(self):
        return camel_to_snake(self.name)


BODY_PARAM = Parameter(
    name="body", kind="Dict[str, Any]", desc=["Request body # TODO "], required=True
)

DELEGATE_PARAM = Parameter(
    name="delegate_to",
    kind="str",
    desc=[
        "The account to impersonate, if any. For this to work, the service account"
        "making the request must have  domain-wide delegation enabled."
    ],
    required=False,
    default=None,
)

GCP_CONN_PARAM = Parameter(
    name="gcp_conn_id",
    kind="str",
    desc=["The connection ID to use when fetching connection info."],
    required=False,
    default="google_cloud_default",
)


def api_param(api_version):
    return Parameter(
        name="api_version",
        kind="str",
        desc=["The version of the api that will be requested for example 'v3'."],
        required=False,
        default=api_version,
    )
