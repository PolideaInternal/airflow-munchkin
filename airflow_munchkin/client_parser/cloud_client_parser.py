# -*- coding: utf-8 -*-
import inspect
from typing import Callable, List, Dict, Optional

from airflow_munchkin.client_parser import docstring_parser
from airflow_munchkin.client_parser.docstring_parser.bricks import FieldBrick, TypeBrick
from airflow_munchkin.client_parser.infos import ParameterInfo, ActionInfo, ClientInfo
from airflow_munchkin.utils import load_class


def parse_method(name: str, method: Callable) -> ActionInfo:
    docstring = method.__doc__
    assert docstring is not None

    doc_sections = docstring_parser.parse_docstring(docstring)
    desc: Optional[List[str]] = None
    args: Dict[str, ParameterInfo] = {}
    return_kind: Optional[TypeBrick] = None
    return_desc: Optional[List[str]] = None
    for i, section in enumerate(doc_sections):
        if i == 0 and section.kind == "Text":
            assert isinstance(section.body, list)
            desc = section.body  # type: ignore
        elif section.kind.lower() in ("args", "arguments", "parameters"):
            for arg in section.body:
                if not isinstance(arg, FieldBrick):
                    raise Exception
                args[arg.name] = ParameterInfo(
                    name=arg.name, kind=arg.type_brick, desc=arg.desc[0].body
                )
        elif section.kind.lower() in ("return", "returns"):
            if not isinstance(section.body, list) or len(section.body) != 1:
                raise Exception
            assert isinstance(section.body[0], FieldBrick)
            field: FieldBrick = section.body[0]
            return_kind = field.type_brick
            return_desc = field.desc[0].body
        else:
            raise Exception(f"Unknown section: {section.kind}")

    assert desc is not None

    return ActionInfo(
        name=name,
        desc=desc,
        args=args,
        return_kind=return_kind,
        return_desc=return_desc,
    )


def parse_client(clazz_name: str) -> ClientInfo:
    clazz = load_class(clazz_name)
    methods = inspect.getmembers(clazz, predicate=inspect.ismethod)
    functions = inspect.getmembers(clazz, predicate=inspect.isfunction)
    path_methods = {
        name: parse_method(name, method)
        for name, method in methods
        if name.endswith("_path")
    }
    action_methods = {
        name: parse_method(name, method)
        for name, method in functions
        if name != "__init__"
    }
    ctor_method = parse_method(
        "__init__", next(method for name, method in functions if name == "__init__")
    )

    return ClientInfo(
        ctor_method=ctor_method,
        path_methods=path_methods,
        action_methods=action_methods,
    )
