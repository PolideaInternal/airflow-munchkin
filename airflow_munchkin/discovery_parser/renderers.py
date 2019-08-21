# -*- coding: utf-8 -*-
import logging
from typing import List

from airflow_munchkin.block_renderer.template_utils import render_template
from airflow_munchkin.discovery_parser.models import DiscoveryIntegration, Operator


def render_single_operator(operator: Operator) -> str:
    return render_template("discovery/class.tpl", {"operator": operator})


def render_operators(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> str:
    operators_classes = [render_single_operator(op) for op in operators]
    content = render_template(
        "discovery/operator_file.tpl",
        {"operators": operators_classes, "integration": integration},
    )
    return content


def render_single_test(operator: Operator, file_name: str) -> str:
    return render_template(
        "discovery/test_class.tpl", {"operator": operator, "file_name": file_name}
    )


def render_tests(operators: List[Operator], file_name) -> str:
    logging.info("Rendering tests file")
    tests = [render_single_test(op, file_name) for op in operators]
    content = render_template(
        "discovery/test_file.tpl",
        {"operators": operators, "tests": tests, "file_name": file_name},
    )
    return content


def render_integration_rst(
    operators: List[Operator], integration: DiscoveryIntegration
) -> str:
    logging.info("Rendering integration.rst file")
    content = render_template(
        "discovery/integration.rst.tpl",
        {"operators": operators, "integration": integration},
    )
    return content


def render_single_example_op(operator: Operator) -> str:
    return render_template("discovery/example_operator.tpl", {"operator": operator})


def render_examples(
    operators: List[Operator], integration: DiscoveryIntegration
) -> str:
    examples = [render_single_example_op(op) for op in operators]
    return render_template(
        "discovery/example_file.tpl",
        {"examples": examples, "integration": integration, "operators": operators},
    )


def render_howto(operators: List[Operator], integration: DiscoveryIntegration) -> str:
    return render_template(
        "discovery/howto.tpl", {"integration": integration, "operators": operators}
    )


def render_system_test(integration: DiscoveryIntegration) -> str:
    key = "GCP_{}_KEY".format(integration.service_name.upper())
    return render_template(
        "discovery/system_test.tpl", {"integration": integration, "key": key}
    )
