# -*- coding: utf-8 -*-
from unittest import TestCase

from airflow_munchkin.block_generator import operator_generator, FileBlock
from airflow_munchkin.integration import Integration


class TestcreateFileBlock(TestCase):
    def test_create_file_block(self):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        result = operator_generator.create_file_block(integration)
        self.assertEqual(
            FileBlock(
                file_name="FILE_PREFFIX_operator.py",
                class_blocks=[],
                import_statement={
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "unittest.TestCase",
                    "typing.Union",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "unittest.mock",
                    "typing.Optional",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "tests.contrib.utils.base_gcp_mock.GCP_PROJECT_ID_HOOK_UNIT_TEST",
                    "typing.Sequence",
                    "typing.Dict",
                    "airflow.AirflowException",
                    "google.api_core.retry.Retry",
                    "typing.Tuple",
                },
                constants=[],
            ),
            result,
        )
