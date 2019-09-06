# -*- coding: utf-8 -*-
import logging
from typing import List

from airflow_munchkin.block_renderer.template_utils import render_template
from airflow_munchkin.discovery_parser.models import (
    DiscoveryIntegration,
    Operator,
    Endpoint,
)


def render_single_hook_method(operator: Operator) -> str:
    return render_template("discovery/hook_method.tpl", {"operator": operator})


def render_hook(
    integration: DiscoveryIntegration, operators: List[Operator], endpoint: Endpoint
) -> str:
    hook_methods = [render_single_hook_method(op) for op in operators]
    content = render_template(
        "discovery/hook_class.tpl",
        {"methods": hook_methods, "integration": integration, "endpoint": endpoint},
    )
    return content


def render_single_hook_test(operator: Operator, package_name: str) -> str:
    return render_template(
        "discovery/test_hook_class.tpl",
        {"operator": operator, "package_name": package_name},
    )


def render_hook_tests(
    integration: DiscoveryIntegration, operators: List[Operator], package_name: str
) -> str:
    tests = [render_single_hook_test(op, package_name) for op in operators]
    content = render_template(
        "discovery/test_hook_file.tpl",
        {
            "tests": tests,
            "integration": integration,
            "hook_class": operators[0].hook_class,
            "package_name": package_name,
        },
    )
    return content


def render_single_operator(operator: Operator) -> str:
    return render_template("discovery/operator_class.tpl", {"operator": operator})


def render_operators(
    integration: DiscoveryIntegration, operators: List[Operator]
) -> str:
    operators_classes = [render_single_operator(op) for op in operators]
    content = render_template(
        "discovery/operator_file.tpl",
        {
            "operators": operators_classes,
            "integration": integration,
            "hook_class": operators[0].hook_class,
        },
    )
    return content


def render_single_test(operator: Operator, package_name: str) -> str:
    return render_template(
        "discovery/test_operator_class.tpl",
        {"operator": operator, "package_name": package_name},
    )


def render_tests(operators: List[Operator], package_name) -> str:
    logging.info("Rendering tests file")
    tests = [render_single_test(op, package_name) for op in operators]
    content = render_template(
        "discovery/test_operator_file.tpl",
        {"operators": operators, "tests": tests, "package_name": package_name},
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
