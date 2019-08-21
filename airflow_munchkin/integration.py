# -*- coding: utf-8 -*-
from typing import NamedTuple

from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class Integration(NamedTuple):
    service_name: str
    class_prefix: str
    file_prefix: str
    client_path: str

    @property
    def client_type_brick(self) -> TypeBrick:
        return TypeBrick(self.client_path)
