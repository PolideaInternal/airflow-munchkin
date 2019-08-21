# -*- coding: utf-8 -*-
import textwrap
from typing import List


def wrap_text(paragraphs: List[str], width: int, deindent_first: bool = False) -> str:
    subsequent_indent = " " * 4 if deindent_first else ""

    paragraph_formatted = []
    for i, paragraph in enumerate(paragraphs):
        paragraph_formatted.append(
            "\n".join(
                textwrap.wrap(
                    paragraph,
                    width,
                    replace_whitespace=False,
                    initial_indent="" if i == 0 else subsequent_indent,
                    subsequent_indent=subsequent_indent,
                )
            )
        )
    return "\n\n".join(paragraph_formatted)


def to_class_name(module_name: str) -> str:
    _, _, name = module_name.rpartition(".")
    return name


def to_package_name(module_name: str) -> str:
    package, _, _ = module_name.rpartition(".")
    return package
