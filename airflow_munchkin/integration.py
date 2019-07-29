# -*- coding: utf-8 -*-
from typing import NamedTuple


class Integration(NamedTuple):
    service_name: str
    class_prefix: str
    file_prefix: str
    client_path: str
