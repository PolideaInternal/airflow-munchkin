# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import ClassBlock
from airflow_munchkin.block_generator.imports_statement_gather import ImportGather
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class TestImportGather(TestCase):
    def test_visit_type_should_remember_import(self):
        gather = ImportGather()
        type_brick = TypeBrick("kitty")
        gather.visit_type(type_brick)
        self.assertEqual({"kitty"}, gather.import_statement)

    def test_visit_type_should_remember_nested_imports(self):
        gather = ImportGather()
        type_brick = TypeBrick("kitty", indexes=[TypeBrick("milk")])
        gather.visit_type(type_brick)
        self.assertEqual({"kitty", "milk"}, gather.import_statement)

    def test_visit_class_should_remember_imports(self):
        gather = ImportGather()
        class_block = ClassBlock(
            name="NAME", extend_class="awesome.cat", methods_blocks=[]
        )
        gather.visit_class(class_block)
        self.assertEqual({"awesome.cat"}, gather.import_statement)


class TestGatherImports(TestCase):
    @mock.patch(  # type: ignore
        "airflow_munchkin.block_generator.imports_statement_gather.ImportGather",
        **{"return_value.import_statement": ["IMPORT_A"]}
    )
    def test_gather_imports(self, mock_import_gather):
        file_block = "FILE_BLOCK"
        mock_import_gather.return_Value.visit_file(file_block)
        result = imports_statement_gather.gather_imports(file_block)
        self.assertEqual(["IMPORT_A"], result)


class TestUpdateImportsStatements(TestCase):
    @mock.patch(
        "airflow_munchkin.block_generator.imports_statement_gather.gather_imports",
        return_value=["IMPORT_A"],
    )  # pylint: disable=no-self-use
    def test_update_imports_statements(self, mock_gather_imports):
        file_block = mock.MagicMock()
        imports_statement_gather.update_imports_statements(file_block)
        mock_gather_imports.assert_called_once_with(file_block)
        file_block.import_statement.update.assert_called_once_with(["IMPORT_A"])
