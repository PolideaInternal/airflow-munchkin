# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator.blocks import (
    CodeBlock,
    MethodBlock,
    ClassBlock,
    FileBlock,
)
from airflow_munchkin.block_renderer import brushes


class TestRenderCodeBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_template",
        return_value="TEMPLATE",
    )
    def test_render_code_block(self, mock_render_template):
        code_block = CodeBlock(
            template_name="TEMPLATE_NAME", template_params={"PARAM_A": "VALUE_A"}
        )
        result = brushes.render_code_block(code_block)
        mock_render_template.assert_called_once_with(
            PARAM_A="VALUE_A", template_name="code_blocks/TEMPLATE_NAME"
        )
        self.assertEqual("TEMPLATE", result)


class TestRenderMethodBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_code_block",
        return_value="TEMPLATE_CODE_BLOCK",
    )
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_template",
        return_value="TEMPLATE",
    )
    def test_render_method_block(self, mock_render_template, mock_render_code_block):
        method_block = MethodBlock(
            name="NAME",
            desc=["DESC_A", "DESC_B"],
            args={"ARG_A": "PARAMETER_A"},
            return_kind="TYPE_BRICK",
            return_desc=["DESC_C", "DESC_D"],
            code_blocks=["CODE_BLOCK_1", "CODE_BLOCK_2"],
            decorator_blocks=["CODE_BLOCK_3", "CODE_BLOCK_4"],
        )
        result = brushes.render_method_block(method_block)
        mock_render_code_block.assert_any_call("CODE_BLOCK_1")
        mock_render_code_block.assert_any_call("CODE_BLOCK_2")
        mock_render_code_block.assert_any_call("CODE_BLOCK_3")
        mock_render_code_block.assert_any_call("CODE_BLOCK_4")
        mock_render_template.assert_called_once_with(
            args={"ARG_A": "PARAMETER_A"},
            code_blocks=["TEMPLATE_CODE_BLOCK", "TEMPLATE_CODE_BLOCK"],
            decorator_blocks=["TEMPLATE_CODE_BLOCK", "TEMPLATE_CODE_BLOCK"],
            desc=["DESC_A", "DESC_B"],
            name="NAME",
            return_desc=["DESC_C", "DESC_D"],
            return_kind="TYPE_BRICK",
            template_name="method_block.py.tpl",
        )
        self.assertEqual("TEMPLATE", result)

    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_code_block",
        return_value="TEMPLATE_CODE_BLOCK",
    )
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_template",
        return_value="TEMPLATE",
    )
    def test_render_ctor_method_block(
        self, mock_render_template, mock_render_code_block
    ):
        method_block = MethodBlock(
            name="__init__",
            desc=["DESC_A", "DESC_B"],
            args={"ARG_A": "PARAMETER_A"},
            return_kind="TYPE_BRICK",
            return_desc=["DESC_C", "DESC_D"],
            code_blocks=["CODE_BLOCK_1", "CODE_BLOCK_2"],
        )
        result = brushes.render_method_block(method_block)
        mock_render_code_block.assert_any_call("CODE_BLOCK_1")
        mock_render_code_block.assert_any_call("CODE_BLOCK_2")
        mock_render_template.assert_called_once_with(
            args={"ARG_A": "PARAMETER_A"},
            code_blocks=["TEMPLATE_CODE_BLOCK", "TEMPLATE_CODE_BLOCK"],
            decorator_blocks=[],
            desc=None,
            name="__init__",
            return_desc=["DESC_C", "DESC_D"],
            return_kind="TYPE_BRICK",
            template_name="method_block.py.tpl",
        )
        self.assertEqual("TEMPLATE", result)


class TestRenderClassBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_method_block",
        return_value="TEMPLATE_METHOD_BLOCK",
    )
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_template",
        return_value="TEMPLATE",
    )
    def test_render_class_block(self, mock_render_template, mock_render_class_block):
        ctor_method = mock.MagicMock()
        ctor_method.name = "__init__"
        method_a = mock.MagicMock()
        method_a.name = "method_a"
        method_b = mock.MagicMock()
        method_b.name = "method_b"
        class_block = ClassBlock(
            name="NAME",
            extend_class="EXTEND_CLASS",
            methods_blocks=[ctor_method, method_a, method_b],
        )
        result = brushes.render_class_block(class_block)
        mock_render_template.assert_called_once_with(
            ctor_method=ctor_method,
            extend_class="EXTEND_CLASS",
            method_blocks=[
                "TEMPLATE_METHOD_BLOCK",
                "TEMPLATE_METHOD_BLOCK",
                "TEMPLATE_METHOD_BLOCK",
            ],
            name="NAME",
            template_name="class_block.py.tpl",
        )
        mock_render_class_block.assert_any_call(method_a)
        mock_render_class_block.assert_any_call(method_b)

        self.assertEqual("TEMPLATE", result)


class TestRenderFileBlock(TestCase):
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_class_block",
        return_value="TEMPLATE_CLASS_BLOCK",
    )
    @mock.patch(
        "airflow_munchkin.block_renderer.brushes.render_template",
        return_value="TEMPLATE",
    )
    def test_render_file_block(self, mock_render_template, mock_render_class_block):
        file_block = FileBlock(
            file_name="FILE_NAME",
            class_blocks=["CLASS_A"],
            import_statement={"kitty", "mouse"},
            constants=["CONSTANT_A"],
        )
        result = brushes.render_file_block(file_block)
        mock_render_template.assert_called_once_with(
            constants=["CONSTANT_A"],
            class_blocks=["TEMPLATE_CLASS_BLOCK"],
            import_statement={"kitty", "mouse"},
            template_name="file_block.py.tpl",
        )
        self.assertEqual("TEMPLATE", result)
