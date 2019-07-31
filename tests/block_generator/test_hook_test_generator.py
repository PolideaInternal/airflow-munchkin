# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator import hook_test_generator
from airflow_munchkin.block_generator.blocks import (
    MethodBlock,
    CodeBlock,
    ClassBlock,
    FileBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
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


class TestGenerateClassBlockWithoutDefaultProjectId(TestCase):
    @mock.patch(f"{BASE_PATH}.generate_setup_method_block", return_value="CLASS_A")
    def test_generate_class_block_without_default_project_id(
        self, mock_generate_setup_method_block
    ):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLIENT_PATH",
        )
        result = hook_test_generator.generate_class_block_without_default_project_id(
            hook_class_path="HOOK_CLASS_PATH", integration=integration
        )
        self.assertEqual(
            ClassBlock(
                name="TestCLASS_PREFIXHook",
                extend_class="unittest.TestCase",
                methods_blocks=["CLASS_A"],
            ),
            result,
        )
        mock_generate_setup_method_block.assert_called_once_with(
            "HOOK_CLASS_PATH", "mock_base_gcp_hook_no_default_project_id"
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
        hook_file_block = FileBlock(
            file_name="FILE_PREFFIX_hook.py",
            class_blocks=[
                ClassBlock(
                    name="CLASS_PREFIXHook",
                    extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    methods_blocks=["METHOD_CTOR", "METHOD_GET_CONN", "METHOD_A"],
                )
            ],
            import_statement={"IMPORT_A"},
        )
        result = hook_test_generator.create_file_block(
            hook_file_block=hook_file_block, integration=integration
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
            "airflow.contrib.hooks.FILE_PREFFIX_hook.CLASS_PREFIXHook", integration
        )
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            result
        )
