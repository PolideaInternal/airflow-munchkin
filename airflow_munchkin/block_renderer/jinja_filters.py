# -*- coding: utf-8 -*-
import textwrap
from typing import List, Union


def wrap_text(
    text: Union[List[str], str], width: int, deindent_first: bool = False
) -> str:
    subsequent_indent = " " * 4 if deindent_first else ""

    if isinstance(text, List):
        paragraph_formatted = [
            "\n".join(
                textwrap.wrap(
                    paragraph,
                    width,
                    initial_indent="" if i == 0 else subsequent_indent,
                    subsequent_indent=subsequent_indent,
                )
            )
            for i, paragraph in enumerate(text)
        ]
        return "\n\n".join(paragraph_formatted)

    return "\n".join(textwrap.wrap(text, width, subsequent_indent=subsequent_indent))


def to_class_name(module_name: str) -> str:
    _, _, name = module_name.rpartition(".")
    return name


def to_package_name(module_name: str) -> str:
    package, _, _ = module_name.rpartition(".")
    return package
