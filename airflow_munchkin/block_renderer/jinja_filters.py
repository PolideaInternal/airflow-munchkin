# -*- coding: utf-8 -*-
import re
import textwrap
from typing import List, Optional
from airflow_munchkin.discovery_parser.utils import camel_to_snake


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


def snake(text: str) -> str:
    return camel_to_snake(text)


def howto(class_name: str) -> str:
    return "howto_{}".format(camel_to_snake(class_name))


def python(variable: Optional[str]) -> Optional[str]:
    return "'{}'".format(variable) if isinstance(variable, str) else variable


def test_constant(param_name: str, param_type: str):
    match = re.findall(r"Optional\[([a-z]+)\]", param_type)
    if match:
        param_type = match[0]
    if param_type == "str":
        return param_name.upper()
    if param_type == "int":
        return 42
    if param_type == "bool":
        return True
    if param_type == "float":
        return 3.1415
    if "Dict" in param_type:
        return {"body": "test"}
    return " # TODO "
