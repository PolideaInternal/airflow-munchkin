# -*- coding: utf-8 -*-
from abc import ABC

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick
from airflow_munchkin.client_parser.infos import ParameterInfo
from airflow_munchkin.block_generator.blocks import (
    FileBlock,
    CodeBlock,
    MethodBlock,
    ClassBlock,
)


class BlockVisitor(ABC):
    """
    Allows you to execute the code for each blocks in the sub-blocks. This class contains the logic of how to
    navigate each type of node.

    In subclasses, overwrite methods for the appropriate type.

    See: https://en.wikipedia.org/wiki/Visitor_pattern
    """

    def visit_import(self, text: str) -> None:
        pass

    def visit_code(self, code_block: CodeBlock) -> None:
        pass

    def visit_method(self, method_block: MethodBlock) -> None:
        for arg in method_block.args.values():
            self.visit_parameter(arg)

        if method_block.return_kind:
            self.visit_type(method_block.return_kind)

    def visit_class(self, class_block: ClassBlock) -> None:
        for method_block in class_block.methods_blocks:
            self.visit_method(method_block)

    def visit_parameter(self, parameter_info: ParameterInfo) -> None:
        if parameter_info.kind:
            self.visit_type(parameter_info.kind)

    def visit_type(self, type_element: TypeBrick) -> None:
        if type_element.indexes:
            for index in type_element.indexes:
                self.visit_type(index)

    def visit_file(self, file_block: FileBlock) -> None:
        for class_block in file_block.class_blocks:
            self.visit_class(class_block)
        for imports in file_block.import_statement:
            self.visit_import(imports)
