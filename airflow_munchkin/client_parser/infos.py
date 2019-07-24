# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Dict, Optional

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class ParameterInfo(NamedTuple):
    name: str
    kind: Optional[TypeBrick]
    desc: List[str]


class ActionInfo(NamedTuple):
    name: str
    desc: List[str]
    args: Dict[str, ParameterInfo]
    return_kind: Optional[TypeBrick]
    return_desc: Optional[List[str]]


class ClientInfo(NamedTuple):
    ctor_method: ActionInfo
    path_methods: Dict[str, ActionInfo]
    action_methods: Dict[str, ActionInfo]
