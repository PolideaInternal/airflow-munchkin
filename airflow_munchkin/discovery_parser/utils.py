# -*- coding: utf-8 -*-
import re
from typing import Optional, List

TYPE_MAP = {
    "string": "str",
    "float": "float",
    "integer": "int",
    "long": "int",
    "boolean": "bool",
    "list": "list",
}


def camel_to_snake(txt: str) -> str:
    """
    Translates CamelCase to snake_.
    """
    sub = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", txt)
    sub = re.sub("([a-z0-9])([A-Z])", r"\1_\2", sub).lower()
    sub = sub.replace("__", "_")
    return sub


def map_type(txt: str) -> Optional[str]:
    return TYPE_MAP.get(txt, None)


def capitalize_first_letter(text: str) -> str:
    return text[0].capitalize() + text[1:]


def split_on_uppers(text: str) -> List[str]:
    return re.findall("[A-Z][^A-Z]*", text) or [text]


def resolve_package_name(service_name: str) -> str:
    parts: List[str] = split_on_uppers(service_name)
    package_name: str = "_".join(p.lower() for p in parts)
    return package_name
