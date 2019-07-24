# -*- coding: utf-8 -*-
import logging
import re
from typing import List, Dict, Callable, Tuple

from sphinx.ext.napoleon.iterators import modify_iter

from airflow_munchkin.client_parser.docstring_parser import typehint_parser
from airflow_munchkin.client_parser.docstring_parser.bricks import (
    TypeBrick,
    FieldBrick,
    SectionBrick,
)

_SECTION_REGEX = re.compile(r"^(\s|\w)+:\s*$")
_TYPED_ARG_REGEX = re.compile(r"\s*(.+?)\s*\(\s*(.*[^\s]+)\s*\)")
_SINGLE_COLON_REGEX = re.compile(r"(?<!:):(?!:)")
_XREF_REGEX = re.compile(r"(:(?:[a-zA-Z0-9]+[\-_+:.])*[a-zA-Z0-9]+:`.+?`)")


class GoogleDocstringParser:  # pylint: disable=too-few-public-methods
    """Parser Google style docstrings to AST.
    Parameters
    ----------
    docstring : :obj:`str`
        The docstring to parse as a string
    Example
    -------
    >>> docstring = '''One line summary.
    ...
    ... Extended description.
    ...
    ... Args:
    ...   arg1(int): Description of `arg1`
    ...   arg2(str): Description of `arg2`
    ... Returns:
    ...   str: Description of return value.
    ... '''
    >>> sections =  GoogleDocstringParser(docstring).sections()
    >>> import pprint
    >>> pprint.pprint(sections)
    [
    Section(kind='Text', body=['One line summary.', '', 'Extended description.', '']),
    Section(kind='Args', body=[
    Field(name='arg1', kind='int', desc=[Section(kind='Text', body=['Description of `arg1`'])]),
    Field(name='arg2', kind='str', desc=[Section(kind='Text', body=['Description of `arg2`'])])
    ]),
    Section(kind='Returns', body=[
    Field(name='', kind='arg2(str)', desc=[Section(kind='Text', body=['Description of return value.'])])])
    ]
    """

    _name_rgx = re.compile(
        r"^\s*((?::(?P<role>\S+):)?`(?P<name>[a-zA-Z0-9_.-]+)`|"
        r" (?P<name2>[a-zA-Z0-9_.-]+))\s*",
        re.X,
    )

    def __init__(self, docstring: str) -> None:
        lines = docstring.splitlines()
        self._line_iter = modify_iter(lines, modifier=lambda s: s.rstrip())
        self._parsed_sections: List[SectionBrick] = []
        self._is_in_section = False
        self._section_indent = 0
        if not hasattr(self, "_sections"):
            self._sections: Dict[str, Callable] = {
                "args": self._parse_parameters_section,
                "arguments": self._parse_parameters_section,
                "parameters": self._parse_parameters_section,
                "return": self._parse_returns_section,
                "returns": self._parse_returns_section,
            }

        self._parse()

    def sections(self) -> List[SectionBrick]:
        """Return the parsed sections of the docstring in reStructuredText format.
        """
        return self._parsed_sections

    def _consume_indented_block(self, indent: int = 1) -> List[str]:
        lines = []
        line = self._line_iter.peek()
        while not self._is_section_break() and (
            not line or self._is_indented(line, indent)
        ):
            lines.append(next(self._line_iter))
            line = self._line_iter.peek()
        return lines

    def _consume_empty(self) -> List[str]:
        lines = []
        line = self._line_iter.peek()
        while self._line_iter.has_next() and not line:
            lines.append(next(self._line_iter))
            line = self._line_iter.peek()
        return lines

    def _consume_field(self) -> Tuple[str, TypeBrick, List[SectionBrick]]:
        line = next(self._line_iter)

        before, _, after = self._partition_field_on_colon(line)
        _name, _type, _desc = before, "", after

        match = _TYPED_ARG_REGEX.match(before)
        if match:
            _name = match.group(1)
            _type = match.group(2)

        _type_element = typehint_parser.parse_typehint(_type)
        indent = self._get_indent(line) + 1
        _descs = [_desc] + self._dedent(self._consume_indented_block(indent))
        _sections = [SectionBrick("Text", self._join_sentences(_descs))]
        return _name, _type_element, _sections

    def _consume_fields(self) -> List[FieldBrick]:
        self._consume_empty()
        fields = []
        while not self._is_section_break():
            _name, _type, _desc = self._consume_field()
            if _name or _type or _desc:
                fields.append(FieldBrick(_name, _type, _desc))
        return fields

    def _consume_returns_section(self) -> List[FieldBrick]:
        lines = self._dedent(self._consume_to_next_section())
        if lines:
            before, colon, after = self._partition_field_on_colon(lines[0])
            _name, _type, _desc = "", "", lines

            if colon:
                if after:
                    _desc = [after] + lines[1:]
                else:
                    _desc = lines[1:]

                _type = before

            _sections = [SectionBrick("Text", self._join_sentences(_desc))]
            _type_element = typehint_parser.parse_typehint(_type) if _type else None
            return [FieldBrick(_name, _type_element, _sections)]
        return []

    def _consume_section_header(self) -> str:
        section: str = next(self._line_iter)
        stripped_section = section.strip(":")
        if stripped_section.lower() in self._sections:
            section = stripped_section
        return section

    def _consume_to_next_section(self) -> List[str]:
        self._consume_empty()
        lines = []
        while not self._is_section_break():
            lines.append(next(self._line_iter))
        self._consume_empty()
        return lines

    def _dedent(self, lines: List[str]) -> List[str]:
        min_indent = self._get_min_indent(lines)
        return [line[min_indent:] for line in lines]

    def _get_current_indent(self, peek_ahead: int = 0) -> int:
        line = self._line_iter.peek(peek_ahead + 1)[peek_ahead]
        while line != self._line_iter.sentinel:
            if line:
                return self._get_indent(line)
            peek_ahead += 1
            line = self._line_iter.peek(peek_ahead + 1)[peek_ahead]
        return 0

    @staticmethod
    def _get_indent(line: str) -> int:
        for i, _chr in enumerate(line):
            if not _chr.isspace():
                return i
        return len(line)

    def _get_min_indent(self, lines: List[str]) -> int:
        min_indent = None
        for line in lines:
            if line:
                indent = self._get_indent(line)
                if min_indent is None:
                    min_indent = indent
                elif indent < min_indent:
                    min_indent = indent
        return min_indent or 0

    @staticmethod
    def _is_indented(line: str, indent: int = 1) -> bool:
        for i, _chr in enumerate(line):
            if i >= indent:
                return True
            if not _chr.isspace():
                return False
        return False

    def _is_section_header(self) -> bool:
        section = self._line_iter.peek().lower()
        match = _SECTION_REGEX.match(section)
        if match:
            header_indent = self._get_indent(section)
            section_indent = self._get_current_indent(peek_ahead=1)
            return section_indent > header_indent
        return False

    def _is_section_break(self) -> bool:
        line = self._line_iter.peek()
        return (
            not self._line_iter.has_next()
            or self._is_section_header()
            or (
                self._is_in_section
                and line
                and not self._is_indented(line, self._section_indent)
            )
        )

    def _parse(self) -> None:
        self._parsed_sections = []
        self._consume_empty()

        while self._line_iter.has_next():
            if self._is_section_header():
                try:
                    section = self._consume_section_header()
                    logging.info('Found section: "%s"', section)
                    if not section.lower() in self._sections:
                        logging.info("Skipping section")
                        self._consume_to_next_section()
                        continue
                    logging.info("Parsing section")
                    self._is_in_section = True
                    self._section_indent = self._get_current_indent()
                    sections = self._sections[section.lower()](section)
                finally:
                    self._is_in_section = False
                    self._section_indent = 0
            else:
                sections = SectionBrick(
                    "Text", self._join_sentences(self._consume_to_next_section())
                )
            self._parsed_sections.append(sections)

    def _parse_parameters_section(self, section: str) -> SectionBrick:
        fields = self._consume_fields()
        return SectionBrick(section, fields)

    def _parse_returns_section(self, section: str) -> SectionBrick:
        fields = self._consume_returns_section()
        return SectionBrick(section, fields)

    @staticmethod
    def _join_sentences(lines: List[str]) -> List[str]:
        if not lines:
            return []
        result = []
        sentence = None
        for line in lines:
            if sentence is None:
                sentence = line
            else:
                if line == "":
                    result.append(sentence)
                    sentence = None
                elif line.startswith("- "):
                    sentence += f"\n{line}"
                else:
                    sentence += " " + line.strip()
        if sentence is not None and sentence != "":
            result.append(sentence)
        return result

    @staticmethod
    def _partition_field_on_colon(line: str) -> Tuple[str, str, str]:
        before_colon = []
        after_colon = []
        colon = ""
        found_colon = False
        for i, source in enumerate(_XREF_REGEX.split(line)):
            if found_colon:
                after_colon.append(source)
            else:
                match = _SINGLE_COLON_REGEX.search(source)
                if (i % 2) == 0 and match:
                    found_colon = True
                    colon = source[match.start() : match.end()]  # noqa: E203
                    before_colon.append(source[: match.start()])
                    after_colon.append(source[match.end() :])  # noqa: E203
                else:
                    before_colon.append(source)

        return "".join(before_colon).strip(), colon, "".join(after_colon).strip()
