# -*- coding: utf-8 -*-
import importlib
import inspect
from typing import Type


def load_class(path: str) -> Type:
    module_name, _, class_name = path.rpartition(".")
    module = importlib.import_module(module_name)
    loaded_class = getattr(module, class_name)

    assert inspect.isclass(loaded_class)

    return loaded_class  # type: ignore
