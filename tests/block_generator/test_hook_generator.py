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
from airflow_munchkin.client_parser.infos import ActionInfo, ParameterInfo, ClientInfo
from airflow_munchkin.integration import Integration


class TestGenerateMethodBlock(TestCase):
    def test_generate_method_block(self):
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
        method_block = hook_generator.generate_method_block(action_info)
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


class TestGenerateCtorMethod(TestCase):
    def test_generate_ctor_method(self):
        ctor_method = self._create_action_info("CTOR_")

        client_info = ClientInfo(
            ctor_method=ctor_method, path_methods={}, action_methods={}
        )
        method_block = hook_generator.generate_ctor_method(client_info=client_info)
        self.assertEqual(
            MethodBlock(
                name="__init__",
                desc=["CTOR_DESC_A", "CTOR_DESC_B"],
                args={
                    "CTOR_ARG_A": ParameterInfo(
                        name="CTOR_ARG_A",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=["CTOR_DESC_C", "CTOR_DESC_D"],
                    )
                },
                return_kind=TypeBrick(kind="float", indexes=[]),
                return_desc=["CTOR_DESC_E", "CTOR_DESC_F"],
                code_blocks=[],
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


class TestGenerateClassBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_ctor_method",
        return_value="METHOD_CTOR",
    )
    @mock.patch(
        "airflow_munchkin.block_generator.hook_generator.generate_method_block",
        return_value="METHOD_A",
    )
    def test_generate_class_block(
        self, mock_generate_method_block, mock_generate_ctor_method
    ):
        integration = Integration(
            class_prefix="CLASS_PREFIX",
            file_prefix="FILE_PREFFIX",
            client_path="CLOENT_PATH",
        )
        ctor_method = self._create_action_info("CTOR_")
        project_path_method = self._create_action_info("PATH_")
        update_instance_method = self._create_action_info("UPDATE_INSTANCE_")
        client_info = ClientInfo(
            ctor_method=ctor_method,
            path_methods={"project_path": project_path_method},
            action_methods={"update_instance": update_instance_method},
        )
        class_block = hook_generator.generate_class_block(
            client_info=client_info, integration=integration
        )
        self.assertEqual(
            ClassBlock(
                name="CLASS_PREFIXHook",
                extend_class="airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                methods_blocks=["METHOD_CTOR", "METHOD_A"],
            ),
            class_block,
        )
        mock_generate_method_block.assert_any_call(update_instance_method)
        mock_generate_ctor_method.assert_called_once_with(client_info)

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
                    "typing.Sequence",
                    "typing.Dict",
                    "google.cloud.redis_v1beta1.CloudRedisClient",
                    "airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook",
                    "google.api_core.retry.Retry",
                    "typing.Optional",
                    "typing.Tuple",
                    "airflow.AirflowException",
                    "typing.Union",
                },
            ),
            file_block,
        )
