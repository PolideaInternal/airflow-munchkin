# -*- coding: utf-8 -*-
from typing import Tuple, Optional, List, Dict
import requests

from airflow_munchkin.discovery_parser.models.integration import DiscoveryIntegration
from airflow_munchkin.discovery_parser.models.method import Method


class Endpoint:
    def __init__(self, integration: DiscoveryIntegration) -> None:
        """
        Representation of single Discovery endpoint.

        :param integration: integration information
        """
        self.integration = integration
        self.service, self.resource_name, methods = self.resolve_service_name(
            integration.api_path
        )
        self.methods = methods or integration.methods

    @staticmethod
    def resolve_service_name(api_path) -> Tuple[str, str, Optional[List[str]]]:
        """
        Returns service name, resource and method from an API path `service_name.resource[.method]`.
        Returned tuple has format:
        (service_name, resource, [methods,])
        """
        splitted: List[str] = api_path.split(".")
        if len(splitted) == 2:
            return splitted[0], splitted[1], None
        if len(splitted) == 3:
            return splitted[0], splitted[1], [splitted[2]]
        raise Exception(
            "The api path is not valid should be in form 'service.resource[.method]'."
        )

    def get_resource(self) -> dict:
        """
        Fetches resource information.
        """
        base_url = "https://www.googleapis.com/discovery/v1/apis/{}/{}/rest"
        url = base_url.format(self.service, self.integration.version)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                "Request to Google APIs resulted in status code: {}".format(
                    response.status_code
                )
            )

        raw_resources: Dict[str, dict] = response.json().get("resources")
        if not raw_resources and not isinstance(raw_resources, dict):
            raise Exception("Obtained resources are not dict: {}".format(raw_resources))

        try:
            return raw_resources[self.resource_name]
        except KeyError:
            raise Exception(
                "No resource named {} in endpoint {}".format(
                    self.resource_name, self.integration.api_path
                )
            )

    def get_methods(self) -> List[Method]:
        """
        Returns list of parsed methods available for the endpoint resource.
        """
        resource = self.get_resource()
        methods = self.methods or resource["methods"].keys()
        return [
            Method.from_dict(m)
            for name, m in resource["methods"].items()
            if name in methods
        ]
