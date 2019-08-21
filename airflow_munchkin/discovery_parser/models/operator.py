# -*- coding: utf-8 -*-
from typing import NamedTuple, List
from copy import deepcopy

from airflow_munchkin.discovery_parser.models.parameter import (
    Parameter,
    DELEGATE_PARAM,
    GCP_CONN_PARAM,
    api_param,
)
from airflow_munchkin.discovery_parser.models.method import Method
from airflow_munchkin.discovery_parser.models.endpoint import Endpoint


class Operator(NamedTuple):
    class_name: str
    description: List[str]
    template_fields: List[str]
    params: List[Parameter]
    data_params: List[Parameter]
    google_api_endpoint_path: str
    google_api_service_name: str
    """
    Representation of a Operator

    :param class_name: name of the operator class
    :param description: description of the operator
    :param template_fields: list of template fields
    :param params: list of parameters that could be passed to the operator
    :param data_params: list of params that could be passed to discovery request
    :param google_api_endpoint_path: discovery API path for a method ex. `dfareporting.campaigns.insert`
    :param google_api_service_name: API service name ex. `dfareporting`
    """

    @classmethod
    def from_endpoint_method(cls, endpoint: Endpoint, method: Method):
        """
        Creates Operator from endpoint and method information.
        """
        params = deepcopy(method.params)
        params.append(api_param(endpoint.integration.version))
        params.append(GCP_CONN_PARAM)
        params.append(DELEGATE_PARAM)

        name = (
            endpoint.integration.class_prefix
            + endpoint.integration.service_name
            + method.name
            + endpoint.integration.object_name
            + "Operator"
        )
        return cls(
            class_name=name,
            description=method.description,
            template_fields=[n.pythonic_name for n in method.params],
            params=params,
            data_params=method.params,
            google_api_endpoint_path=".".join(
                [endpoint.service, endpoint.resource_name, method.name]
            ),
            google_api_service_name=endpoint.service,
        )


def endpoint_to_operators(endpoint: Endpoint) -> List[Operator]:
    """
    Generates list of operators for a given endpoint.
    """
    operators = [
        Operator.from_endpoint_method(endpoint, method)
        for method in endpoint.get_methods()
    ]
    return operators
