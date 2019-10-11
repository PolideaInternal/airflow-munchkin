# -*- coding: utf-8 -*-
import logging
from typing import Set

from airflow_munchkin.block_generator.blocks import ClassBlock, FileBlock
from airflow_munchkin.block_generator.block_visitor import BlockVisitor
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class ImportGather(BlockVisitor):
    def __init__(self) -> None:
        self.import_statement: Set[str] = set()

    def visit_type(self, type_element: TypeBrick) -> None:
        super().visit_type(type_element)
        self.remember_import_statement(type_element.kind)

    def visit_class(self, class_block: ClassBlock) -> None:
        super().visit_class(class_block)
        self.remember_import_statement(class_block.extend_class)

    def remember_import_statement(self, statement: str) -> None:
        if statement in ("str", "float", "str", "int", "dict", "None", "bool"):
            return

        if statement in (
            "Sequence",
            "Union",
            "Optional",
            "Tuple",
            "Dict",
            "Set",
            "List",
            "Iterator",
            "Iterable",
        ):
            statement = f"typing.{statement}"
        self.import_statement.add(statement)


def gather_imports(file_block: FileBlock) -> Set[str]:
    visitor = ImportGather()
    visitor.visit_file(file_block)
    return visitor.import_statement


def update_imports_statements(file_block: FileBlock) -> None:
    logging.info("Start gathering import statements")
    import_statement = gather_imports(file_block)
    file_block.import_statement.update(import_statement)
    logging.info(
        "Finished import statements. Found %s statements", len(import_statement)
    )
