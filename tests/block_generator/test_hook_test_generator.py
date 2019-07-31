# -*- coding: utf-8 -*-
from typing import List
from unittest import TestCase, mock

from airflow_munchkin.block_generator import hook_test_generator
from airflow_munchkin.block_generator.blocks import (
    MethodBlock,
    CodeBlock,
    ClassBlock,
    FileBlock,
    ParameterBlock,
)
from airflow_munchkin.client_parser import ClientInfo
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import ActionInfo
from airflow_munchkin.integration import Integration

BASE_PATH = "airflow_munchkin.block_generator.hook_test_generator"


class TestGenerateSetupMethodBlock(TestCase):
    def test_generate_setup_method_block(self):
        result = hook_test_generator.generate_setup_method_block(
            class_path="CLASS_PATH", init_new="INIT_NEW"
        )
        self.assertEqual(
            MethodBlock(
                name="setUp",
                desc=None,
                args={},
                return_kind=TypeBrick(kind="None", indexes=[]),
                return_desc=None,
                code_blocks=[
                    CodeBlock(
                        template_name="setup_mock.py.tpl",
                        template_params={"class_path": "CLASS_PATH", "new": "INIT_NEW"},
                    )
                ],
                decorator_blocks=[],
            ),
            result,
        )


class TestGenerateTestMethodForClientCall(TestCase):
    def test_generate_test_method_for_client_call(self):
        action_info = self._create_action("ACTION", ["ARG_1", "ARG_2"])
        method_block = self._create_method("METHOD", ["ARG_2", "ARG_3"])
        hook_class_path = "HOOK_CLASS_PATH"

        result = hook_test_generator.generate_test_method_for_client_call(
            action_info, method_block, hook_class_path
        )
        self.assertEqual(
            MethodBlock(
                name="test_METHOD",
                desc=None,
                args={
                    "mock_get_conn": ParameterBlock(
                        name="mock_get_conn", kind=None, desc=None, default_value=None
                    )
                },
                return_kind=TypeBrick(kind="None", indexes=[]),
                return_desc=None,
                code_blocks=[
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "target": "self.hook.METHOD",
                            "call_params": {
                                "ARG_2": "TEST_ARG_2",
                                "ARG_3": "TEST_ARG_3",
                            },
                        },
                    ),
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "target": "mock_get_conn.ACTION.assert_called_once_with",
                            "call_params": {
                                "ARG_1": "TEST_ARG_1",
                                "ARG_2": "TEST_ARG_2",
                            },
                        },
                    ),
                ],
                decorator_blocks=[
                    CodeBlock(
                        template_name="decorator_mock_get_conn.py.tpl",
                        template_params={"class_path": "HOOK_CLASS_PATH"},
                    )
                ],
            ),
            result,
        )

    @staticmethod
    def _create_action(name: str, args: List[str]):
        return ActionInfo(
            name=name,
            desc=[],
            args={a: mock.MagicMock() for a in args},
            return_kind=None,
            return_desc=None,
        )

    @staticmethod
    def _create_method(name: str, args: List[str]):
        return MethodBlock(
            name=name,
            desc=None,
            args={a: mock.MagicMock() for a in args},
            return_kind=None,
            return_desc=None,
            code_blocks=[],
            decorator_blocks=[],
        )


class TestgenerateTestMethodForCallWithoutProjectId(TestCase):
    def test_generate_test_method_for_call_without_project_id(self):
        hook_class_path = "HOOK_CLASS_PATH"
        hook_method = self._create_method("METHOD_A", ["ARG_A", "ARG_B"])
        result = hook_test_generator.generate_test_method_for_call_without_project_id(
            hook_class_path, hook_method
        )
        self.assertEqual(
            MethodBlock(
                name="test_METHOD_A_without_project_id",
                desc=None,
                args={
                    "mock_get_conn": ParameterBlock(
                        name="mock_get_conn", kind=None, desc=None, default_value=None
                    )
                },
                return_kind=TypeBrick(kind="None", indexes=[]),
                return_desc=None,
                code_blocks=[
                    CodeBlock(
                        template_name="method_call_assert_raises.py.tpl",
                        template_params={
                            "target": "self.hook.METHOD_A",
                            "call_params": {
                                "ARG_A": "TEST_ARG_A",
                                "ARG_B": "TEST_ARG_B",
                            },
                        },
                    )
                ],
                decorator_blocks=[
                    CodeBlock(
                        template_name="decorator_mock_get_conn.py.tpl",
                        template_params={"class_path": "HOOK_CLASS_PATH"},
                    )
                ],
            ),
            result,
        )

    @staticmethod
    def _create_method(name: str, args: List[str]):
        return MethodBlock(
            name=name,
            desc=None,
            args={a: mock.MagicMock() for a in args},
            return_kind=None,
            return_desc=None,
            code_blocks=[],
            decorator_blocks=[],
        )


class TestGenerateClassBlockWithoutDefaultProjectId(TestCase):
    @mock.patch(
        f"{BASE_PATH}.generate_test_method_for_call_without_project_id",
        return_value="TEST_C",
    )
    @mock.patch(
        f"{BASE_PATH}.generate_test_method_for_client_call",
        side_effect=["TEST_A", "TEST_B"],
    )
    @mock.patch(f"{BASE_PATH}.generate_setup_method_block", return_value="CLASS_A")
    def test_generate_class_block_without_default_project_id(
        self,
        mock_generate_setup_method_block,
        mock_generate_test_method_for_client_call,
        mock_generate_test_method_for_call_without_project_id,
    ):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLIENT_PATH",
        )

        method_a = self._create_method("METHOD_A", args=["location"])
        method_b = self._create_method("METHOD_B", args=["project_id"])
        action_a = self._create_action("METHOD_A")
        action_b = self._create_action("METHOD_B")

        result = hook_test_generator.generate_class_block_without_default_project_id(
            hook_class_path="HOOK_CLASS_PATH",
            hook_class=ClassBlock(
                name="CLASS_PREFIXHook",
                extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                methods_blocks=[method_a, method_b],
            ),
            client_info=ClientInfo(
                ctor_method=None,
                path_methods={},
                action_methods={"METHOD_A": action_a, "METHOD_B": action_b},
            ),
            integration=integration,
        )
        self.assertEqual(
            ClassBlock(
                name="TestCLASS_PREFIXHook",
                extend_class="unittest.TestCase",
                methods_blocks=["CLASS_A", "TEST_A", "TEST_B", "TEST_C"],
            ),
            result,
        )
        mock_generate_setup_method_block.assert_called_once_with(
            "HOOK_CLASS_PATH", "mock_base_gcp_hook_no_default_project_id"
        )
        mock_generate_test_method_for_client_call.assert_any_call(
            action_a, method_a, "HOOK_CLASS_PATH"
        )
        mock_generate_test_method_for_client_call.assert_any_call(
            action_b, method_b, "HOOK_CLASS_PATH"
        )
        mock_generate_test_method_for_call_without_project_id.assert_any_call(
            "HOOK_CLASS_PATH", method_b
        )

    @staticmethod
    def _create_method(name: str, args: List[str]):
        return MethodBlock(
            name=name,
            desc=None,
            args={a: mock.MagicMock() for a in args},
            return_kind=None,
            return_desc=None,
            code_blocks=[],
            decorator_blocks=[],
        )

    @staticmethod
    def _create_action(name: str):
        return ActionInfo(
            name=name, desc=[], args={}, return_kind=None, return_desc=None
        )


class TestCreateFileBlock(TestCase):
    @mock.patch(f"{BASE_PATH}.imports_statement_gather")
    @mock.patch(
        f"{BASE_PATH}.generate_class_block_without_default_project_id",
        return_value="CLASS_A",
    )
    def test_create_file_block(
        self,
        mock_generate_class_block_without_default_project_id,
        mock_imports_statement_gather,
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
        result = hook_test_generator.create_file_block(
            hook_file_block=hook_file_block,
            integration=integration,
            client_info="CLIENT_INFO",
        )
        self.assertEqual(
            FileBlock(
                file_name="test_FILE_PREFFIX_hook.py",
                class_blocks=["CLASS_A"],
                import_statement={
                    "typing.Dict",
                    "airflow.AirflowException",
                    "typing.Union",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "google.api_core.retry.Retry",
                    "typing.Sequence",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "unittest.TestCase",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "typing.Tuple",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "unittest.mock",
                    "airflow.contrib.hooks.FILE_PREFFIX_hook.CLASS_PREFIXHook",
                    "typing.Optional",
                },
            ),
            result,
        )
        mock_generate_class_block_without_default_project_id.assert_called_once_with(
            "airflow.contrib.hooks.FILE_PREFFIX_hook.CLASS_PREFIXHook",
            hook_class_block,
            "CLIENT_INFO",
            integration,
        )
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            result
        )
