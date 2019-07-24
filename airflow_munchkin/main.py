# -*- coding: utf-8 -*-

"""Main module."""
import logging
from typing import List

from airflow_munchkin import client_parser, block_renderer, block_generator
from airflow_munchkin.block_generator import FileBlock
from airflow_munchkin.client_parser.infos import ClientInfo
from airflow_munchkin.integration import Integration


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    integration_info: Integration = Integration(
        class_prefix="CloudMemorystore",
        file_prefix="gcp_cloud_memorystore",
        client_path="google.cloud.redis_v1.CloudRedisClient",
    )

    client_info: ClientInfo = client_parser.parse_cloud_client(integration_info)
    file_blocks: List[FileBlock] = block_generator.generate_file_blocks(
        client_info=client_info, integration=integration_info
    )
    block_renderer.create_files_from_file_blocks(file_blocks)


if __name__ == "__main__":
    main()
