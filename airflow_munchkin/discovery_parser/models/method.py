# -*- coding: utf-8 -*-
from typing import NamedTuple, List
from airflow_munchkin.discovery_parser.models.parameter import Parameter, BODY_PARAM


class Method(NamedTuple):
    name: str
    description: List[str]
    params: List[Parameter]
    """
    :param name: name of the method ex. list, get, create
    :param description: description of the method. Required in form of a list for textwrap.
    :param params: parameters that could be passed to the method.
    """

    @classmethod
    def from_dict(cls, method: dict):
        """
        Creates `Method` from dictionary in form of
        ```
        {
            "id": "doubleclicksearch.reports.get",
            "path": "reports/{reportId}",
            "httpMethod": "GET",
            "description": "Polls for the status of a report request.",
            "parameters": {
                "reportId": {
                    "type": "string",
                    "description": "ID of the report request being polled.",
                    "required": True,
                    "location": "path",
                }
            },
            "parameterOrder": ["reportId"],
            "response": {"$ref": "Report"},
            "scopes": ["https://www.googleapis.com/auth/doubleclicksearch"],
        }
        ```

        """
        name = method["id"].split(".")[-1]
        params = [
            Parameter.from_dict(name, info)
            for name, info in method.get("parameters", {}).items()
        ]
        if method["httpMethod"] == "POST":
            params.append(BODY_PARAM)
        params.sort(key=lambda p: p.required, reverse=True)
        return cls(
            name=name.capitalize(), params=params, description=[method["description"]]
        )
