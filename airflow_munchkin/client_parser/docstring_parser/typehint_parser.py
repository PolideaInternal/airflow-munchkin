# -*- coding: utf-8 -*-
import logging
import re
from typing import List, Optional

from sphinx.ext.napoleon.iterators import peek_iter

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


# pylint: disable=too-few-public-methods
class TypeHintParser:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.hint_iter: Optional[peek_iter] = None
        self.element: Optional[TypeBrick] = None
        self._parse()

    def _assert_has_next(self) -> None:
        assert self.hint_iter is not None

        if self.hint_iter.has_next():
            raise Exception("Unexpected end of text")

    def _consume_whitespace(self) -> None:
        assert self.hint_iter is not None

        while self.hint_iter.has_next() and self.hint_iter.peek().isspace():
            self.hint_iter.next()

    def _read_kind(self) -> str:
        assert self.hint_iter is not None

        self._consume_whitespace()
        if self.hint_iter.peek() == "~":
            self.hint_iter.next()
        kind = ""
        while self.hint_iter.has_next() and (
            self.hint_iter.peek().isalpha()
            or self.hint_iter.peek().isdigit()
            or self.hint_iter.peek() in (".", "_", "|")
        ):
            kind += self.hint_iter.next()
        return kind

    def _read_type_list(self) -> List[TypeBrick]:
        assert self.hint_iter is not None

        self.hint_iter.next()  # Consume [
        elements: List[TypeBrick] = []
        while self.hint_iter.has_next() and self.hint_iter.peek() != "]":
            self._consume_whitespace()
            elements.append(self._read_type_element())
            self._consume_whitespace()
            if self.hint_iter.peek() == ",":
                self.hint_iter.next()

        self.hint_iter.next()  # Consume ]
        return elements

    def _read_type_element(self) -> TypeBrick:
        assert self.hint_iter is not None

        kind = self._read_kind()
        indexes: List[TypeBrick] = []
        if self.hint_iter.has_next() and self.hint_iter.peek() == "[":
            indexes = self._read_type_list()
        return TypeBrick(kind, indexes)

    @staticmethod
    def _fix_incorrect_typehints(text: str) -> str:
        # Example value: dict[str -> str]
        match_invalid_dict = re.match(r"^[Dd]ict\[\s*(.+)\s+->\s+(.+)\s*\]$", text)
        if match_invalid_dict:
            # Result: Dict[str, str]
            return f"Dict[{match_invalid_dict.group(1)}, {match_invalid_dict.group(2)}]"
        return text

    def _parse(self) -> None:
        self.text = self._fix_incorrect_typehints(self.text)
        self.hint_iter = peek_iter(self.text)
        if not self.hint_iter.has_next():
            raise Exception("Empty value. You should provide a text to parse")

        element = self._read_type_element()

        if self.hint_iter.has_next():
            raise Exception(
                "Unexpected end of processing. Parsing has stopped, but there are still characters to "
                "process."
            )
        self.element = element


def replace_all_kind(typehint_element: TypeBrick, old: str, new: str):
    def walk_recursive_and_replace(element: TypeBrick):
        if element.kind == old:
            element.kind = new
        if element.indexes:
            for child in element.indexes:
                walk_recursive_and_replace(child)

    walk_recursive_and_replace(typehint_element)


def replace_deprecated_union_style(typehint_element: TypeBrick):
    def walk_recursive_and_replace(element: TypeBrick):
        if not element.indexes and "|" in element.kind:
            element.indexes = [
                TypeBrick(kind=index.strip()) for index in element.kind.split("|")
            ]
            element.kind = "Union"
        if element.indexes:
            for child in element.indexes:
                walk_recursive_and_replace(child)

    walk_recursive_and_replace(typehint_element)


def parse_typehint(text: str) -> TypeBrick:
    logging.info("Parsing typehint: %s", text)
    parser = TypeHintParser(text)
    assert parser.element is not None
    element = parser.element
    replace_deprecated_union_style(element)
    replace_all_kind(element, "dict", "Dict")
    replace_all_kind(element, "set", "Set")
    replace_all_kind(element, "list", "List")
    replace_all_kind(element, "iterator", "Iterator")

    return element
