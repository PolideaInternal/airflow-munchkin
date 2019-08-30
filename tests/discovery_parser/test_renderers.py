# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.discovery_parser.models import (
    Operator,
    Parameter,
    Method,
    DiscoveryIntegration,
)
from airflow_munchkin.discovery_parser.renderers import (
    render_single_operator,
    render_single_test,
    render_operators,
    render_tests,
    render_system_test,
    render_integration_rst,
    render_examples,
    render_howto,
    render_single_example_op,
)

# pylint:disable=line-too-long


class TestRenderers(TestCase):
    def setUp(self) -> None:
        params = [
            Parameter("param1", "str", ["Param 1 description"], True),
            Parameter("param2", "int", ["Param 2 description"], False),
        ]
        method = Method("magic", ["Performs magic tasks in cloud."], params)
        self.op = Operator(
            class_name="ClassName",
            description=["some nice description"],
            template_fields=["field1", "field2"],
            params=params,
            data_params=params,
            hook_class="HookClass",
            google_api_version="v1000",
            resource_name="resource",
            method=method,
        )
        self.integration = DiscoveryIntegration(
            api_path="service.method",
            version="v3",
            service_name="TestService",
            object_name="report",
            package_name="test",
        )

    def test_render_single_operator(self):
        content = render_single_operator(self.op)
        expected = '''class ClassName(BaseOperator):
    """
    some nice description

    .. seealso::
        For more information on how to use this operator, take a look at the guide:
        :ref:`howto/operator:ClassName`

    :param param1: Param 1 description
    :type param1: str
    :param param2: Param 2 description
    :type param2: int
    """
    template_fields = ("field1", "field2", )

    @apply_defaults
    def __init__(
        self,
        param1: str,
        param2: int = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.param1 = param1
        self.param2 = param2

    def execute(self, context):
        hook = HookClass(
            gcp_conn_id=self.gcp_conn_id,
            delegate_to=self.delegate_to,
            api_version=self.api_version,
        )
        response = hook.magic(
            param1=self.param1,
            param2=self.param2,
        )
        return response
'''
        self.assertEqual(expected, content)

    @mock.patch(
        "airflow_munchkin.discovery_parser.renderers.render_single_operator",
        return_value="XXX",
    )
    def test_render_operators(
        self, render_single_mock
    ):  # pylint:disable=unused-argument
        content = render_operators(self.integration, [self.op, self.op])
        expected = '''"""
This module contains Google TestService operators.
"""
from typing import Tuple, List, Any, Dict, Optional

from airflow.utils.decorators import apply_defaults
from airflow.models.baseoperator import BaseOperator
from airflow.gcp.hooks.test import HookClass


XXX

XXX

'''
        self.assertEqual(expected, content)

    def test_render_single_test(self):
        content = render_single_test(self.op, "file_name")
        expected = """class TestClassName(TestCase):
    @mock.patch('airflow.gcp.operators.file_name.HookClass', )
    @mock.patch('airflow.gcp.operators.file_name.BaseOperator', )
    def test_execute(self, mock_base_op, hook_mock):
        param1 = 'PARAM1'
        param2 = 42
        op = ClassName(
    param1=param1,
    param2=param2,
            api_version=API_VERSION,
            task_id="test_task"
        )
        op.execute(context=None)
        hook_mock.assert_called_once_with(
            gcp_conn_id=GCP_CONN_ID,
            delegate_to=None,
            api_version=API_VERSION,
        )
        hook_mock.return_value.magic.assert_called_once_with(
            param1 = param1,
            param2 = param2,
        )
"""
        self.assertEqual(expected, content)

    @mock.patch(
        "airflow_munchkin.discovery_parser.renderers.render_single_test",
        return_value="XXX",
    )
    def test_render_tests(self, render_single_mock):  # pylint:disable=unused-argument
        content = render_tests([self.op, self.op], "package_name")
        expected = """from unittest import TestCase, mock
from airflow.gcp.operators.package_name import (ClassName, ClassName, )

API_VERSION = 'api_version'
GCP_CONN_ID = 'google_cloud_default'


XXX

XXX

"""
        self.assertEqual(expected, content)

    def test_render_system_test(self):
        content = render_system_test(self.integration)
        expected = """import unittest
from tests.contrib.utils.base_gcp_system_test_case import SKIP_TEST_WARNING, DagGcpSystemTestCase
from tests.contrib.utils.gcp_authenticator import GCP_TESTSERVICE_KEY


@unittest.skipIf(DagGcpSystemTestCase.skip_check(GCP_TESTSERVICE_KEY), SKIP_TEST_WARNING)
class TestServiceSystemTest(DagGcpSystemTestCase):
    def __init__(self, method_name="runTest"):
        super().__init__(
            method_name, dag_id="example_test", gcp_key=GCP_TESTSERVICE_KEY
        )

    def test_run_example_dag(self):
        self._run_dag()"""
        self.assertEqual(expected, content)

    def test_render_integration(self):
        content = render_integration_rst([self.op, self.op], self.integration)
        expected = """TestService
'''''''''

:class:`airflow.gcp.operators.test.ClassName`
    some nice description

:class:`airflow.gcp.operators.test.ClassName`
    some nice description


They also use :class:`airflow.gcp.hooks.test.HookClass` to communicate with Google Cloud Platform."""  # noqa
        self.assertEqual(expected, content)

    def test_render_single_example_op(self):
        content = render_single_example_op(self.op)
        expected = """# [START howto_class_name]
class_name_task = ClassName(
    param1=param1,
    task_id="class_name_task",
)
# [END howto_class_name]"""
        self.assertEqual(expected, content)

    @mock.patch(
        "airflow_munchkin.discovery_parser.renderers.render_single_example_op",
        return_value="XXX",
    )
    def test_render_examples(
        self, render_single_mock
    ):  # pylint:disable=unused-argument
        content = render_examples([self.op, self.op], self.integration)
        expected = '''"""
Example Airflow DAG that shows how to use TestService.
"""

from airflow.utils import dates
from airflow import models
from airflow.gcp.operators.test import (ClassName, ClassName, )

# [START howto_test_env_variables]
# TODO
# [END howto_test_env_variables]

default_args = {"start_date": dates.days_ago(1)}

with models.DAG(
    "example_test", default_args=default_args, schedule_interval=None  # Override to match your needs
) as dag:
    XXX

    XXX

'''
        self.assertEqual(expected, content)

    def test_render_howto(self):
        content = render_howto([self.op], self.integration)
        expected = """Google TestService Operators
=======================================

Here goes a copy pasted text from service website.

.. contents::
  :depth: 1
  :local:

Prerequisite Tasks
^^^^^^^^^^^^^^^^^^

.. include:: _partials/prerequisite_tasks.rst

.. _howto/operator:ClassName:

A section title
^^^^^^^^^^^^^^^

Here describe how to use :class:`~airflow.gcp.operators.test.ClassName`.

.. exampleinclude:: ../../../../airflow/gcp/example_dags/example_test.py
    :language: python
    :dedent: 4
    :start-after: [START howto_class_name]
    :end-before: [END howto_class_name]

You can use :ref:`Jinja templating <jinja-templating>` with
:template-fields:`airflow.gcp.operators.test.ClassName`
parameters which allows you to dynamically determine values.
The result is saved to :ref:`XCom <concepts:xcom>`, which allows it to be used by other operators.

"""
        self.assertEqual(expected, content)
