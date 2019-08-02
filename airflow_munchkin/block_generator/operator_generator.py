# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.block_generator import imports_statement_gather
from airflow_munchkin.block_generator.blocks import FileBlock
from airflow_munchkin.integration import Integration


def create_file_block(integration: Integration) -> FileBlock:
    logging.info("Start creating operators file block")
    file_block: FileBlock = FileBlock(
        file_name=f"{integration.file_prefix}_operator.py", class_blocks=[]
    )
    imports_statement_gather.update_imports_statements(file_block)
    logging.info("Finished creating operators file block")
    return file_block
