# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator.block_visitor import BlockVisitor


class DummyBlockVisitor(BlockVisitor):
    pass


class TestBlockVisitor(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_code"
    )
    def test_visit_import(self, mock_visit_code):
        visitor = DummyBlockVisitor()
        mock_import = mock.MagicMock()
        visitor.visit_import(mock_import)
        self.assertEqual(mock_import.call_count, 0)

    def test_visit_code(self):
        visitor = DummyBlockVisitor()
        mock_code = mock.MagicMock()
        visitor.visit_code(mock_code)
        self.assertEqual(mock_code.call_count, 0)

    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_parameter"
    )
    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_type"
    )
    def test_visit_method(
        self, mock_visit_type, mock_visit_parameter
    ):  # pylint: disable=no-self-use
        visitor = DummyBlockVisitor()
        method_block = mock.MagicMock(
            **{
                "args.values.return_value": ["ARG_A", "ARG_B"],
                "return_kind": "RETURN_KIND",
            }
        )
        visitor.visit_method(method_block)
        mock_visit_type.assert_called_once_with("RETURN_KIND")
        mock_visit_parameter.assert_any_call("ARG_A")
        mock_visit_parameter.assert_any_call("ARG_B")

    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_method"
    )  # pylint: disable=no-self-use
    def test_visit_class(self, mock_visit_method):
        visitor = DummyBlockVisitor()
        method_block = mock.MagicMock(**{"methods_blocks": ["METHOD_A", "METHOD_B"]})
        visitor.visit_class(method_block)
        mock_visit_method.assert_any_call("METHOD_A")
        mock_visit_method.assert_any_call("METHOD_B")

    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_type"
    )  # pylint: disable=no-self-use
    def test_visit_parameter(self, mock_visit_type):
        visitor = DummyBlockVisitor()
        method_block = mock.MagicMock(**{"kind": "TYPE_A"})
        visitor.visit_parameter(method_block)
        mock_visit_type.assert_any_call("TYPE_A")

    def test_visit_type(self):
        # TODO: Write this case
        self.assertTrue(True)  # pylint: disable=redundant-unittest-assert

    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_import"
    )
    @mock.patch(
        "airflow_munchkin.block_generator.block_visitor.BlockVisitor.visit_class"
    )
    def test_visit_file(
        self, mock_visit_class, mock_visit_import
    ):  # pylint: disable=no-self-use
        visitor = DummyBlockVisitor()
        method_block = mock.MagicMock(
            **{
                "class_blocks": ["CLASS_A", "CLASS_B"],
                "import_statement": ["IMPORT_A", "IMPORT_B"],
            }
        )
        visitor.visit_file(method_block)
        mock_visit_class.assert_any_call("CLASS_A")
        mock_visit_class.assert_any_call("CLASS_B")
        mock_visit_import.assert_any_call("IMPORT_A")
        mock_visit_import.assert_any_call("IMPORT_B")
        mock_visit_import.assert_any_call("IMPORT_B")
