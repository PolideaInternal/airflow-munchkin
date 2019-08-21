# -*- coding: utf-8 -*-
from typing import Dict, Optional, List

from airflow_munchkin.block_generator.blocks import Constant
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


def generate_constant_list(
    unique_constant: Dict[str, Optional[TypeBrick]]
) -> List[Constant]:
    constants = []
    for name, kind in unique_constant.items():
        constant_name = f"TEST_{name.upper()}"
        constant_kind = kind or TypeBrick("None")
        if constant_kind and (constant_kind.is_union or constant_kind.is_optional):
            constant_kind = constant_kind.indexes[0]
        constant_value = (
            f'\'test-{name.replace("_", "-")}\''
            if constant_kind.name == "str"
            else "None # TODO: Fill missing value"
        )
        constants.append(
            Constant(name=constant_name, kind=constant_kind, value=constant_value)
        )
    return constants
