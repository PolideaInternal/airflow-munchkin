# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator import hook_generator
from airflow_munchkin.block_generator.blocks import (
    CodeBlock,
    MethodBlock,
    ClassBlock,
    FileBlock,
    ParameterBlock,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import (
    ActionInfo,
    ParameterInfo,
    ClientInfo,
    PathInfo,
)
from airflow_munchkin.integration import Integration


class TestGenerateMethodBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.convert_path_"
        "parameter_block_to_individual_parameters",
        return_value=(
            {
                "location": ParameterBlock(
                    name="location",
                    kind=TypeBrick(kind="str", indexes=[]),
                    desc=["TODO: Fill description"],
                    default_value=None,
                )
            },
            {
                "project_id": ParameterBlock(
                    name="project_id",
                    kind=TypeBrick(kind="str", indexes=[]),
                    desc=["TODO: Fill description"],
                    default_value="None",
                )
            },
            CodeBlock(
                template_name="call_path.py.tpl",
                template_params={
                    "var_name": "parent",
                    "fn_name": "location",
                    "args": ["project_id", "location"],
                    "client": TypeBrick(kind="CLOENT_PATH", indexes=[]),
                },
            ),
        ),
    )
    def test_generate_method_block(
        self, mock_convert_path_parameter_block_to_individual_parameters
    ):
        action_info = ActionInfo(
            name="NAME",
            desc=["DESC_A", "DESC_B"],
            args={
                "ARG_A": ParameterInfo(
                    name="ARG_A", kind=TypeBrick("str"), desc=["DESC_C", "DESC_D"]
                )
            },
            return_kind=TypeBrick("float"),
            return_desc=["DESC_E", "DESC_F"],
        )
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        method_block = hook_generator.generate_method_block(
            action_info, path_infos="PATH_INFOS", integration=integration
        )
        self.assertEqual(
            MethodBlock(
                name="NAME",
                desc=["DESC_A", "DESC_B"],
                args={
                    "ARG_A": ParameterBlock(
                        name="ARG_A",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=["DESC_C", "DESC_D"],
                    )
                },
                return_kind=TypeBrick(kind="float", indexes=[]),
                return_desc=["DESC_E", "DESC_F"],
                code_blocks=[
                    CodeBlock(template_name="client_init.py.tpl", template_params={}),
                    CodeBlock(
                        template_name="client_call.py.tpl",
                        template_params={
                            "var_name": "result",
                            "name": "NAME",
                            "call_params": {"ARG_A": "ARG_A"},
                        },
                    ),
                    CodeBlock(
                        template_name="return.py.tpl",
                        template_params={"var_name": "result"},
                    ),
                ],
            ),
            method_block,
        )


class TestGenerateGetConnMethodBlock(TestCase):
    def test_generate_method_block(self):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        method_block = hook_generator.generate_get_conn_method_block(integration)
        self.assertEqual(
            MethodBlock(
                name="get_conn",
                desc=[
                    "Retrieves client library object that allow access to SERVICE_NAME service."
                ],
                args={},
                return_kind=TypeBrick(kind="CLOENT_PATH", indexes=[]),
                return_desc=["SERVICE_NAME client object."],
                code_blocks=[
                    CodeBlock(
                        template_name="get_conn_body.py.tpl",
                        template_params={
                            "client": TypeBrick(kind="CLOENT_PATH", indexes=[])
                        },
                    )
                ],
            ),
            method_block,
        )

    @staticmethod
    def _create_action_info(prefix: str):
        return ActionInfo(
            name=f"{prefix}NAME",
            desc=[f"{prefix}DESC_A", f"{prefix}DESC_B"],
            args={
                f"{prefix}ARG_A": ParameterInfo(
                    name=f"{prefix}ARG_A",
                    kind=TypeBrick("str"),
                    desc=[f"{prefix}DESC_C", f"{prefix}DESC_D"],
                )
            },
            return_kind=TypeBrick("float"),
            return_desc=[f"{prefix}DESC_E", f"{prefix}DESC_F"],
        )


class TestGenerateCtorMethodBlock(TestCase):
    def test_generate_method_block(self):
        client_info = mock.MagicMock(**{"ctor_method.desc": ["DESC_A", "DESC_B"]})
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        method_block = hook_generator.generate_ctor_method_block(
            client_info, integration
        )
        self.assertEqual(
            MethodBlock(
                name="__init__",
                desc=["DESC_A", "DESC_B"],
                args={
                    "gcp_conn_id": ParameterBlock(
                        name="gcp_conn_id",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=None,
                        default_value=None,
                    ),
                    "delegate_to": ParameterBlock(
                        name="delegate_to",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=None,
                        default_value=None,
                    ),
                },
                return_kind=TypeBrick(kind="None", indexes=[]),
                return_desc=None,
                code_blocks=[
                    CodeBlock(
                        template_name="super_call.py.tpl",
                        template_params={
                            "args": ["gcp_conn_id", "delegate_to"],
                            "kwargs": {},
                        },
                    ),
                    CodeBlock(
                        template_name="set_field.py.tpl",
                        template_params={
                            "field_name": "_client",
                            "field_type": TypeBrick(kind="CLOENT_PATH", indexes=[]),
                            "field_value": "None",
                        },
                    ),
                ],
            ),
            method_block,
        )


class TestConvertPathParameter(TestCase):
    def test_should_convert(self):
        parameter = ParameterInfo(
            name="parent",
            kind=TypeBrick(kind="str", indexes=[]),
            desc=[
                "Required. The resource name of the instance location using the form: "
                "``projects/{project_id}/locations/{location_id}`` where "
                "``location_id`` refers to a GCP region"
            ],
        )
        path_infos = {
            "location": PathInfo(name="location", args=["project", "location"])
        }
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        req_params, opt_params, code = hook_generator.convert_path_parameter_block_to_individual_parameters(
            parameter, path_infos=path_infos, integration=integration
        )

        self.assertEqual(
            {
                "location": ParameterBlock(
                    name="location",
                    kind=TypeBrick(kind="str", indexes=[]),
                    desc=["TODO: Fill description"],
                    default_value=None,
                )
            },
            req_params,
        )
        self.assertEqual(
            {
                "project_id": ParameterBlock(
                    name="project_id",
                    kind=TypeBrick(kind="str", indexes=[]),
                    desc=["TODO: Fill description"],
                    default_value="None",
                )
            },
            opt_params,
        )
        self.assertEqual(
            CodeBlock(
                template_name="call_path.py.tpl",
                template_params={
                    "var_name": "parent",
                    "fn_name": "location",
                    "args": ["project_id", "location"],
                    "client": TypeBrick(kind="CLOENT_PATH", indexes=[]),
                },
            ),
            code,
        )


class TestGenerateClassBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_ctor_method_block",
        return_value="METHOD_CTOR",
    )
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_get_conn_method_block",
        return_value="METHOD_GET_CONN",
    )
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_method_block",
        return_value="METHOD_A",
    )
    def test_generate_class_block(
        self,
        mock_generate_method_block,
        mock_generate_get_conn_method_block,
        mock_generate_ctor_method_block,
    ):
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        ctor_method = self._create_action_info("CTOR_")
        update_instance_method = self._create_action_info("UPDATE_INSTANCE_")
        client_info = ClientInfo(
            ctor_method=ctor_method,
            path_methods={},
            action_methods={"update_instance": update_instance_method},
        )
        class_block = hook_generator.generate_class_block(
            client_info=client_info, integration=integration
        )
        self.assertEqual(
            ClassBlock(
                name="CLASS_PREFIXHook",
                extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                methods_blocks=["METHOD_CTOR", "METHOD_GET_CONN", "METHOD_A"],
            ),
            class_block,
        )
        mock_generate_method_block.assert_any_call(
            update_instance_method, path_infos={}, integration=integration
        )
        mock_generate_ctor_method_block.assert_called_once_with(
            client_info, integration
        )
        mock_generate_get_conn_method_block.assert_called_once_with(integration)
        mock_generate_ctor_method_block.assert_called_once_with(
            client_info, integration
        )

    @staticmethod
    def _create_action_info(prefix: str):
        return ActionInfo(
            name=f"{prefix}NAME",
            desc=[f"{prefix}DESC_A", f"{prefix}DESC_B"],
            args={
                f"{prefix}ARG_A": ParameterInfo(
                    name=f"{prefix}ARG_A",
                    kind=TypeBrick("str"),
                    desc=[f"{prefix}DESC_C", f"{prefix}DESC_D"],
                )
            },
            return_kind=TypeBrick("float"),
            return_desc=[f"{prefix}DESC_E", f"{prefix}DESC_F"],
        )


class TestCreateFileBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.imports_statement_gather",
        return_value="CLASS_A",
    )
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_class_block",
        return_value="CLASS_A",
    )
    def test_create_file_block(
        self, mock_generate_class_block, mock_imports_statement_gather
    ):
        client_info = "CLIENT_INFO"
        integration = Integration(
            service_name="SERVICE_NAME",
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        file_block = hook_generator.create_file_block(client_info, integration)
        mock_generate_class_block.assert_called_once_with(client_info, integration)
        mock_imports_statement_gather.update_imports_statements.assert_called_once_with(
            mock.ANY
        )
        self.assertEqual(
            FileBlock(
                file_name="FILE_PREFFIX_hook.py",
                class_blocks=["CLASS_A"],
                import_statement={
                    "typing.Union",
                    "typing.Optional",
                    "typing.Sequence",
                    "typing.Tuple",
                    "typing.Dict",
                    "airflow.AirflowException",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "google.api_core.retry.Retry",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_default_project_id",
                    "tests.contrib.utils.base_gcp_mock.mock_base_gcp_hook_no_default_project_id",
                    "unittest.TestCase",
                    "unittest.mock",
                },
            ),
            file_block,
        )
