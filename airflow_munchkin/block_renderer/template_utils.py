# -*- coding: utf-8 -*-
"""Template utilities"""
import inspect

import jinja2
from jinja2 import Template

from airflow_munchkin.block_renderer import jinja_filters, jinja_functions
from airflow_munchkin.config import TEMPLATE_PATH

TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath=TEMPLATE_PATH)
TEMPLATE_ENV = jinja2.Environment(
    loader=TEMPLATE_LOADER,
    undefined=jinja2.StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Load filters and functions
TEMPLATE_ENV.filters.update(
    {
        name: fn
        for name, fn in inspect.getmembers(jinja_filters, predicate=inspect.isfunction)
    }
)
TEMPLATE_ENV.globals.update(
    {
        name: fn
        for name, fn in inspect.getmembers(
            jinja_functions, predicate=inspect.isfunction
        )
    }
)


def render_template(template_name: str, *args, **kwargs) -> str:
    """Render Jinja template"""
    template: Template = TEMPLATE_ENV.get_template(template_name)
    content: str = template.render(*args, **kwargs)
    return content
