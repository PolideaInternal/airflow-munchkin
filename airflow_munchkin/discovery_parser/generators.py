# -*- coding: utf-8 -*-
import logging
from os import path
from typing import List

from airflow_munchkin.discovery_parser.models import DiscoveryIntegration, Operator
from airflow_munchkin.config import OUTPUT_PATH
from airflow_munchkin.block_renderer import cosmetics

from airflow_munchkin.discovery_parser.renderers import (
    render_howto,
    render_examples,
    render_integration_rst,
    render_tests,
    render_operators,
    render_system_test,
)


def generate_operators(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> None:
    logging.info("Rendering python file")
    content = render_operators(integration, operators)

    output_file_name: str = path.join(OUTPUT_PATH, integration.package_name)
    output_file_name += ".py"

    logging.info("Saving operators to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)

    cosmetics.apply_cosmetics(output_file_name)


def generate_tests(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> None:
    output_file_name = "test_" + integration.package_name + ".py"
    output_file_name = path.join(OUTPUT_PATH, output_file_name)
    content = render_tests(operators, integration.package_name)

    logging.info("Saving tests to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)
    cosmetics.apply_cosmetics(output_file_name)


def generate_integration_rst(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> None:
    output_file_name = "integration_" + integration.package_name + ".rst"
    output_file_name = path.join(OUTPUT_PATH, output_file_name)
    content = render_integration_rst(operators, integration)

    logging.info("Saving integration info to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)


def generate_examples(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> None:
    output_file_name = "example_" + integration.package_name + ".py"
    output_file_name = path.join(OUTPUT_PATH, output_file_name)
    content = render_examples(operators, integration)

    logging.info("Saving example DAG to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)
    cosmetics.apply_cosmetics(output_file_name)


def generate_howto(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> None:
    output_file_name = integration.package_name + ".rst"
    output_file_name = path.join(OUTPUT_PATH, output_file_name)
    content = render_howto(operators, integration)

    logging.info("Saving how to guide to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)


def generate_system_test(integration: DiscoveryIntegration) -> None:
    output_file_name = "test_" + integration.package_name + "_system.py"
    output_file_name = path.join(OUTPUT_PATH, output_file_name)
    content = render_system_test(integration)

    logging.info("Saving system test to %s", output_file_name)
    with open(output_file_name, "w") as file:
        file.write(content)
    cosmetics.apply_cosmetics(output_file_name)
