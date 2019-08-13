# -*- coding: utf-8 -*-
import logging

from airflow_munchkin.client_parser import cloud_client_parser
from airflow_munchkin.client_parser.infos import ClientInfo
from airflow_munchkin.integration import Integration


def parse_cloud_client(integration: Integration) -> ClientInfo:
    logging.info("Start parsing library class")

    client_info = cloud_client_parser.parse_client(integration.client_path)

    logging.info(
        "Finished parsing library class, Found %s action method, %s path methods",
        len(client_info.action_methods),
        len(client_info.path_methods),
    )

    return client_info
