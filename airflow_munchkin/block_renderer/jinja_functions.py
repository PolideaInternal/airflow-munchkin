# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import List

from airflow_munchkin.block_renderer.jinja_filters import wrap_text


def rst_param(name: str, desc: List[str], width: int):
    prefix: str = f":param {name}:"
    paragraphs = deepcopy(desc)
    if not desc:
        return prefix
    paragraphs[0] = f"{prefix} {paragraphs[0]}"

    return wrap_text(paragraphs, width, deindent_first=True)
