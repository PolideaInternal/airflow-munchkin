# -*- coding: utf-8 -*-
import logging
from typing import List

from airflow_munchkin.block_generator import (
    hook_generator,
    hook_test_generator,
    operator_generator,
)
from airflow_munchkin.block_generator.blocks import FileBlock
from airflow_munchkin.client_parser import ClientInfo
from airflow_munchkin.integration import Integration


def generate_file_blocks(
    client_info: ClientInfo, integration: Integration
) -> List[FileBlock]:
    logging.info("Start generating file blocks")

    # Hooks
    hook_file_block = hook_generator.create_file_block(client_info, integration)
    hook_test_file_block = hook_test_generator.create_file_block(
        hook_file_block, client_info, integration
    )

    # Operators
    operator_file_block = operator_generator.create_file_block(
        integration, hook_file_block
    )

    logging.info("Finish generating file blocks")
    return [hook_file_block, hook_test_file_block, operator_file_block]
