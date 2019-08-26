# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.discovery_parser.models import DiscoveryIntegration, Endpoint
from airflow_munchkin.discovery_parser.generators import (
    generate_hook,
    generate_hook_tests,
    generate_operators,
    generate_tests,
    generate_integration_rst,
    generate_examples,
    generate_howto,
    generate_system_test,
)
from airflow_munchkin.discovery_parser.models.operator import endpoint_to_operators
from airflow_munchkin.discovery_parser.utils import resolve_package_name


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    service_name = "SearchAds"
    integration = DiscoveryIntegration(
        api_path="dfareporting.accountUserProfiles",
        version="v3.2",
        service_name=service_name,
        object_name="Profile",
        package_name=resolve_package_name(service_name),
    )
    endp = Endpoint(integration)

    logging.info("Parsing endpoint to operators")
    operators = endpoint_to_operators(endp)

    generate_hook(integration, operators, endp)
    generate_hook_tests(integration, operators)
    generate_operators(integration, operators)
    generate_tests(integration, operators)
    generate_integration_rst(integration, operators)
    generate_examples(integration, operators)
    generate_howto(integration, operators)
    generate_system_test(integration)


if __name__ == "__main__":
    main()
