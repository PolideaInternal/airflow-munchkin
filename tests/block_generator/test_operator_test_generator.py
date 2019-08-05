# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator import operator_test_generator
from airflow_munchkin.block_generator.blocks import ClassBlock, FileBlock
from airflow_munchkin.integration import Integration


BASE_PATH = "airflow_munchkin.block_generator.operator_test_generator"


class TestCreateFileBlock(TestCase):
    @mock.patch(f"{BASE_PATH}.imports_statement_gather")
    def test_create_file_block(self, mock_imports_statement_gather):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        operator_a = self._create_operator_class_block("OperatorA")
        operator_b = self._create_operator_class_block("OperatorB")
        hook_file_block = FileBlock(
            file_name="FILE_PREFFIX_hook.py",
            class_blocks=[operator_a, operator_b],
            import_statement={"IMPORT_A"},
        )
        result = operator_test_generator.create_file_block(hook_file_block, integration)
        self.assertEqual(
            FileBlock(
                file_name="test_FILE_PREFFIX_operator.py",
                class_blocks=[],
                import_statement={
                    "typing.Union",
                    "google.api_core.retry.Retry",
                    "tests.contrib.utils.base_gcp_mock.GCP_PROJECT_ID_HOOK_UNIT_TEST",
                    "typing.Dict",
                    "typing.Sequence",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "unittest.TestCase",
                    "typing.Optional",
                    "unittest.mock",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "airflow.utils.decorators.apply_defaults",
                    "airflow.AirflowException",
                    "airflow.contrib.operator.FILE_PREFFIX_hook.OperatorB",
                    "typing.Tuple",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "airflow.contrib.operator.FILE_PREFFIX_hook.OperatorA",
                },
                constants=[],
            ),
            result,
        )
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            result
        )

    @staticmethod
    def _create_operator_class_block(name):
        return ClassBlock(name=name, extend_class="EXTEND_CLASS", methods_blocks=[])
