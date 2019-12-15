# -*- coding: utf-8 -*-
from typing import List
from unittest import TestCase, mock

from airflow_munchkin.block_generator import operator_generator
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    MethodBlock,
    FileBlock,
    ParameterBlock,
    CodeBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.integration import Integration


BASE_PATH = "airflow_munchkin.block_generator.operator_generator"


class TestCreateOperatorClassBlock(TestCase):
    def test_create_operator_class_block(self):
        hook_class_name = "HOOK_CLASS_NAME"
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        hook_method = self._create_method("METHOD_A", ["arg_a", "arg_b"])
        result = operator_generator.create_operator_class_block(
            hook_class_name, hook_method, integration=integration
        )
        self.assertEqual(
            ClassBlock(
                name="CLASS_PREFIXMethodAOperator",
                extend_class="airflow.models.BaseOperator",
                methods_blocks=[
                    MethodBlock(
                        name="__init__",
                        desc=None,
                        args={
                            "arg_a": ParameterBlock(
                                name="arg_a", kind=None, desc=None, default_value=None
                            ),
                            "arg_b": ParameterBlock(
                                name="arg_b", kind=None, desc=None, default_value=None
                            ),
                            "gcp_conn_id": ParameterBlock(
                                name="gcp_conn_id",
                                kind=TypeBrick(kind="str"),
                                desc=None,
                                default_value="'google_cloud_default'",
                            ),
                            "*args": ParameterBlock(
                                name="*args", kind=None, desc=None, default_value=None
                            ),
                            "**kwargs": ParameterBlock(
                                name="**kwargs",
                                kind=None,
                                desc=None,
                                default_value=None,
                            ),
                        },
                        return_kind=TypeBrick(kind="None"),
                        return_desc=None,
                        code_blocks=[
                            CodeBlock(
                                template_name="super_call.py.tpl",
                                template_params={
                                    "args": ["*args", "**kwargs"],
                                    "kwargs": {},
                                },
                            ),
                            CodeBlock(
                                template_name="set_field.py.tpl",
                                template_params={
                                    "field_name": "arg_a",
                                    "field_value": "arg_a",
                                    "field_type": None,
                                },
                            ),
                            CodeBlock(
                                template_name="set_field.py.tpl",
                                template_params={
                                    "field_name": "arg_b",
                                    "field_value": "arg_b",
                                    "field_type": None,
                                },
                            ),
                            CodeBlock(
                                template_name="set_field.py.tpl",
                                template_params={
                                    "field_name": "gcp_conn_id",
                                    "field_value": "gcp_conn_id",
                                    "field_type": None,
                                },
                            ),
                        ],
                        decorator_blocks=[
                            CodeBlock(
                                template_name="decorator_apply_defaults.py.tpl",
                                template_params={},
                            )
                        ],
                    ),
                    MethodBlock(
                        name="execute",
                        desc=None,
                        args={
                            "context": ParameterBlock(
                                name="context",
                                kind=TypeBrick(kind="Dict"),
                                desc=None,
                                default_value=None,
                            )
                        },
                        return_kind=None,
                        return_desc=None,
                        code_blocks=[
                            CodeBlock(
                                template_name="method_call.py.tpl",
                                template_params={
                                    "var_name": "hook",
                                    "target": "HOOK_CLASS_NAME",
                                    "call_params": {"gcp_conn_id": "self.gcp_conn_id"},
                                },
                            ),
                            CodeBlock(
                                template_name="method_call.py.tpl",
                                template_params={
                                    "target": "hook.METHOD_A",
                                    "call_params": {
                                        "arg_a": "self.arg_a",
                                        "arg_b": "self.arg_b",
                                    },
                                },
                            ),
                        ],
                        decorator_blocks=[],
                    ),
                ],
            ),
            result,
        )

    @staticmethod
    def _create_method(name: str, args: List[str]):
        return MethodBlock(
            name=name,
            desc=None,
            args={a: ParameterBlock(a) for a in args},
            return_kind=None,
            return_desc=None,
            code_blocks=[],
            decorator_blocks=[],
        )


class TestCreateOperatorClassBlocks(TestCase):
    @mock.patch(
        f"{BASE_PATH}.create_operator_class_block", side_effect=["CLASS_A", "CLASS_B"]
    )
    def test_create_operator_class_blocks(self, mock_create_operator_class_block):
        method_a = self._create_method("METHOD_A")
        method_b = self._create_method("METHOD_B")

        hook_class_block = ClassBlock(
            name="CLASS_PREFIXHook",
            extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
            methods_blocks=[method_a, method_b],
        )

        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )

        result = operator_generator.create_operator_class_blocks(
            hook_class_block, integration
        )
        self.assertEqual(["CLASS_A", "CLASS_B"], result)

    @mock.patch(f"{BASE_PATH}.create_operator_class_block", side_effect=["CLASS_A"])
    def test_should_skip_ctor(self, mock_create_operator_class_block):
        method_a = self._create_method("__init__")
        method_b = self._create_method("METHOD_A")

        hook_class_block = ClassBlock(
            name="CLASS_PREFIXHook",
            extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
            methods_blocks=[method_a, method_b],
        )

        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )

        result = operator_generator.create_operator_class_blocks(
            hook_class_block, integration
        )
        self.assertEqual(["CLASS_A"], result)

    @mock.patch(f"{BASE_PATH}.create_operator_class_block", side_effect=["CLASS_A"])
    def test_should_skip_get_conn(self, mock_create_operator_class_block):
        method_a = self._create_method("get_conn")
        method_b = self._create_method("METHOD_A")

        hook_class_block = ClassBlock(
            name="CLASS_PREFIXHook",
            extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
            methods_blocks=[method_a, method_b],
        )

        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )

        result = operator_generator.create_operator_class_blocks(
            hook_class_block, integration
        )
        self.assertEqual(["CLASS_A"], result)

    @staticmethod
    def _create_method(name: str):
        return MethodBlock(
            name=name,
            desc=None,
            args={},
            return_kind=None,
            return_desc=None,
            code_blocks=[],
            decorator_blocks=[],
        )


class TestCreateFileBlock(TestCase):
    @mock.patch(f"{BASE_PATH}.imports_statement_gather")
    @mock.patch(
        f"{BASE_PATH}.create_operator_class_blocks", return_value=["CLASS_A", "CLASS_B"]
    )
    def test_create_file_block(
        self, mock_create_operator_class_blocks, mock_imports_statement_gather
    ):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        hook_class_block = ClassBlock(
            name="CLASS_PREFIXHook",
            extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
            methods_blocks=["METHOD_CTOR", "METHOD_GET_CONN", "METHOD_A"],
        )
        hook_file_block = FileBlock(
            file_name="FILE_PREFFIX_hook.py",
            class_blocks=[hook_class_block],
            import_statement={"IMPORT_A"},
        )
        result = operator_generator.create_file_block(integration, hook_file_block)
        self.assertEqual(
            FileBlock(
                file_name="FILE_PREFFIX_operator.py",
                class_blocks=["CLASS_A", "CLASS_B"],
                import_statement={
                    "typing.Tuple",
                    "typing.Union",
                    "typing.Optional",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "unittest.mock",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "airflow.utils.decorators.apply_defaults",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "airflow.contrib.hooks.FILE_PREFFIX_hook.CLASS_PREFIXHook",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "typing.Dict",
                    "tests.contrib.utils.base_gcp_mock.GCP_PROJECT_ID_HOOK_UNIT_TEST",
                    "airflow.AirflowException",
                    "google.api_core.retry.Retry",
                    "typing.Sequence",
                    "unittest.TestCase",
                },
                constants=[],
            ),
            result,
        )
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            result
        )
        mock_create_operator_class_blocks.assert_called_once_with(
            hook_class_block, integration
        )
