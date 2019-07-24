# -*- coding: utf-8 -*-
import logging
import textwrap
from typing import List

from airflow_munchkin.client_parser.docstring_parser.bricks import SectionBrick
from airflow_munchkin.client_parser.docstring_parser.google_docstring_parser import (
    GoogleDocstringParser,
)


def parse_docstring(docstring: str) -> List[SectionBrick]:
    logging.info("Start parsing docstring")
    parser = GoogleDocstringParser(textwrap.dedent(docstring))
    logging.info("Finished parsing docstring")
    return parser.sections()
