# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator import operator_test_generator
from airflow_munchkin.block_generator.blocks import (
    ClassBlock,
    FileBlock,
    MethodBlock,
    ParameterBlock,
    CodeBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.integration import Integration


BASE_PATH = "airflow_munchkin.block_generator.operator_test_generator"


class TestFindClientCallMethodName(TestCase):
    def test_find_client_call_method_name(self):
        operator_class_block = ClassBlock(
            name="CloudMemorystoreCreateInstanceOperator",
            extend_class="airflow.models.BaseOperator",
            methods_blocks=[
                MethodBlock(
                    name="execute",
                    desc=None,
                    args={},
                    return_kind=None,
                    return_desc=None,
                    code_blocks=[
                        CodeBlock(
                            template_name="method_call.py.tpl",
                            template_params={"target": "CloudMemorystoreHook"},
                        ),
                        CodeBlock(
                            template_name="method_call.py.tpl",
                            template_params={
                                "target": "hook.create_instance",
                                "call_params": {},
                            },
                        ),
                    ],
                    decorator_blocks=[],
                )
            ],
        )
        result = operator_test_generator.find_client_call_method_name(
            operator_class_block
        )
        self.assertEqual("create_instance", result)


class TestCreateAssertCallMethodBlock(TestCase):
    @mock.patch(f"{BASE_PATH}.find_client_call_method_name", return_value="METHOD_NAME")
    def test_create_assert_call_method_block(self, mock_find_client_call_method_name):
        operator_module_path = "OPERATOR_MODULE_PATH"
        hook_class_name = "CloudMemorystoreHook"
        operator_class_block = ClassBlock(
            name="CloudMemorystoreCreateInstanceOperator",
            extend_class="airflow.models.BaseOperator",
            methods_blocks=[
                MethodBlock(
                    name="__init__",
                    desc=[
                        "Creates a Redis instance based on the specified tier and memory size."
                    ],
                    args={
                        "location": ParameterBlock(
                            name="location",
                            kind=TypeBrick(kind="str"),
                            desc=["TODO: Fill description"],
                            default_value=None,
                        ),
                        "instance_id": ParameterBlock(
                            name="instance_id", kind=TypeBrick(kind="str")
                        ),
                        "instance": ParameterBlock(
                            name="instance",
                            kind=TypeBrick(
                                kind="Union",
                                indexes=[
                                    TypeBrick(kind="Dict"),
                                    TypeBrick(
                                        kind="google.cloud.redis_v1.types.Instance"
                                    ),
                                ],
                            ),
                        ),
                        "project_id": ParameterBlock(
                            name="project_id",
                            kind=TypeBrick(kind="str"),
                            desc=["TODO: Fill description"],
                            default_value="None",
                        ),
                        "retry": ParameterBlock(
                            name="retry",
                            kind=TypeBrick(kind="google.api_core.retry.Retry"),
                            default_value="None",
                        ),
                        "timeout": ParameterBlock(
                            name="timeout",
                            kind=TypeBrick(kind="float"),
                            default_value="None",
                        ),
                        "metadata": ParameterBlock(
                            name="metadata",
                            kind=TypeBrick(
                                kind="Sequence",
                                indexes=[
                                    TypeBrick(
                                        kind="Tuple",
                                        indexes=[
                                            TypeBrick(kind="str"),
                                            TypeBrick(kind="str"),
                                        ],
                                    )
                                ],
                            ),
                            default_value="None",
                        ),
                        "gcp_conn_id": ParameterBlock(
                            name="gcp_conn_id",
                            kind=TypeBrick(kind="str"),
                            desc=None,
                            default_value="'google_cloud_default'",
                        ),
                        "*args": ParameterBlock(name="*args"),
                        "**kwargs": ParameterBlock(name="**kwargs"),
                    },
                    return_kind=TypeBrick(kind="None"),
                    return_desc=None,
                    code_blocks=[],
                    decorator_blocks=[],
                )
            ],
        )
        result = operator_test_generator.create_assert_call_method_block(
            operator_module_path, hook_class_name, operator_class_block
        )
        self.assertEqual(
            MethodBlock(
                name="test_assert_valid_hook_call",
                desc=None,
                args={"mock_hook": ParameterBlock(name="mock_hook")},
                return_kind=TypeBrick(kind="None"),
                return_desc=None,
                code_blocks=[
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "var_name": "task",
                            "target": "CloudMemorystoreCreateInstanceOperator",
                            "call_params": {
                                "location": "TEST_LOCATION",
                                "instance_id": "TEST_INSTANCE_ID",
                                "instance": "TEST_INSTANCE",
                                "project_id": "TEST_PROJECT_ID",
                                "retry": "TEST_RETRY",
                                "timeout": "TEST_TIMEOUT",
                                "metadata": "TEST_METADATA",
                                "gcp_conn_id": "TEST_GCP_CONN_ID",
                            },
                        },
                    ),
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "target": "task.execute",
                            "call_params": {"context": "mock.MagicMock()"},
                        },
                    ),
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "target": "mock_hook.assert_called_once_with",
                            "call_params": {"gcp_conn_id": "TEST_GCP_CONN_ID"},
                        },
                    ),
                    CodeBlock(
                        template_name="method_call.py.tpl",
                        template_params={
                            "target": "mock_hook.return_value.METHOD_NAME.assert_called_once_with",
                            "call_params": {
                                "location": "TEST_LOCATION",
                                "instance_id": "TEST_INSTANCE_ID",
                                "instance": "TEST_INSTANCE",
                                "project_id": "TEST_PROJECT_ID",
                                "retry": "TEST_RETRY",
                                "timeout": "TEST_TIMEOUT",
                                "metadata": "TEST_METADATA",
                            },
                        },
                    ),
                ],
                decorator_blocks=[
                    CodeBlock(
                        template_name="decorator_mock_hook.py.tpl",
                        template_params={
                            "class_path": "OPERATOR_MODULE_PATH.CloudMemorystoreHook"
                        },
                    )
                ],
            ),
            result,
        )
        mock_find_client_call_method_name.assert_called_once_with(operator_class_block)


class TestCreateOperatorTestClassBlocks(TestCase):
    @staticmethod
    @mock.patch(
        f"{BASE_PATH}.create_assert_call_method_block", return_value="CONSTANTS"
    )
    def test_create_operator_test_class_blocks(mock_create_assert_call_method_block):
        operator_module_path = "OPERATOR_MODULE_PATH"
        hook_class_name = "HOOK_CLASS_NAME"
        operator_class = ClassBlock(
            name="CLASS", extend_class="EXTEND_CLASS", methods_blocks=[]
        )
        operator_test_generator.create_operator_test_class_blocks(
            operator_module_path=operator_module_path,
            hook_class_name=hook_class_name,
            operator_class=operator_class,
        )
        mock_create_assert_call_method_block.assert_called_once_with(
            operator_module_path, hook_class_name, operator_class
        )


class TestCreateConstants(TestCase):
    @mock.patch(
        f"{BASE_PATH}.constant_generator.generate_constant_list",
        return_value="CONSTANTS",
    )
    def test_create_constants(self, mock_generate_constant_list):
        class_a = ClassBlock(
            name="CLASS",
            extend_class="EXTEND_CLASS",
            methods_blocks=[
                MethodBlock(
                    name="__init__",
                    desc=None,
                    args={"ARG_A": ParameterBlock("ARG_A", kind=TypeBrick("str"))},
                    return_kind=None,
                    return_desc=None,
                    code_blocks=[],
                    decorator_blocks=[],
                )
            ],
        )
        class_b = ClassBlock(
            name="CLASS",
            extend_class="EXTEND_CLASS",
            methods_blocks=[
                MethodBlock(
                    name="__init__",
                    desc=None,
                    args={
                        "ARG_B": ParameterBlock("ARG_B"),
                        "*args": ParameterBlock("*args"),
                        "**kwargs": ParameterBlock("**kwargs"),
                    },
                    return_kind=None,
                    return_desc=None,
                    code_blocks=[],
                    decorator_blocks=[],
                ),
                MethodBlock(
                    name="execute",
                    desc=None,
                    args={"ARG_C": ParameterBlock("ARG_C")},
                    return_kind=None,
                    return_desc=None,
                    code_blocks=[],
                    decorator_blocks=[],
                ),
            ],
        )
        result = operator_test_generator.create_constants([class_a, class_b])
        self.assertEqual("CONSTANTS", result)
        mock_generate_constant_list.assert_called_once_with(
            {"ARG_A": TypeBrick(kind="str"), "ARG_B": None}
        )


class TestCreateFileBlock(TestCase):
    @mock.patch(f"{BASE_PATH}.create_constants", return_value="CONSTANTS")
    @mock.patch(
        f"{BASE_PATH}.create_operator_test_class_blocks",
        side_effect=["CLASS_A", "CLASS_B"],
    )
    @mock.patch(f"{BASE_PATH}.imports_statement_gather")
    def test_create_file_block(
        self,
        mock_imports_statement_gather,
        mock_create_operator_test_class_blocks,
        mock_create_constants,
    ):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        operator_a = self._create_operator_class_block("OperatorA")
        operator_b = self._create_operator_class_block("OperatorB")

        operator_file_block = FileBlock(
            file_name="FILE_PREFFIX_operator.py",
            class_blocks=[operator_a, operator_b],
            import_statement={"IMPORT_A"},
        )
        hook_file_block = FileBlock(
            file_name="FILE_PREFFIX_hook.py",
            class_blocks=[operator_a, operator_b],
            import_statement={"IMPORT_A"},
        )

        result = operator_test_generator.create_file_block(
            operator_file_block, hook_file_block, integration
        )
        self.assertEqual(
            FileBlock(
                file_name="test_FILE_PREFFIX_operator.py",
                class_blocks=["CLASS_A", "CLASS_B"],
                import_statement={
                    "typing.Tuple",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "typing.Sequence",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "tests.contrib.utils.base_gcp_mock.GCP_PROJECT_ID_HOOK_UNIT_TEST",
                    "airflow.utils.decorators.apply_defaults",
                    "airflow.AirflowException",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "typing.Optional",
                    "typing.Dict",
                    "unittest.TestCase",
                    "airflow.contrib.operator.FILE_PREFFIX_operator.OperatorB",
                    "google.api_core.retry.Retry",
                    "unittest.mock",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "airflow.contrib.operator.FILE_PREFFIX_operator.OperatorA",
                    "typing.Union",
                },
                constants="CONSTANTS",
            ),
            result,
        )
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            result
        )

    @staticmethod
    def _create_operator_class_block(name):
        return ClassBlock(name=name, extend_class="EXTEND_CLASS", methods_blocks=[])
