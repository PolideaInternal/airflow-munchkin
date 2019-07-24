# -*- coding: utf-8 -*-

"""Main module."""
import logging

from airflow_munchkin import client_parser

from airflow_munchkin.client_parser.infos import ClientInfo
from airflow_munchkin.integration import Integration


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    integration_info: Integration = Integration(
        class_prefix="Cloud Memorystore",
        file_prefix="gcp_cloud_memorystore",
        client_path="google.cloud.redis_v1.CloudRedisClient",
    )

    client_info: ClientInfo = client_parser.parse_cloud_client(integration_info)
    print(client_info)


if __name__ == "__main__":
    main()
