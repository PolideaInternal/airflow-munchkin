# -*- coding: utf-8 -*-
"""
This module contains a Google Compute Engine Hook.
"""

from typing import Any, Optional

from googleapiclient.discovery import build

from airflow import AirflowException
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook


class GceHook(GoogleCloudBaseHook):
    """
    Hook for Google Compute Engine APIs.

    All the methods in the hook where project_id is used must be called with
    keyword arguments rather than positional.
    """

    _conn = None  # type: Optional[Any]

    def __init__(
        self,
        api_version: str = "v1",
        gcp_conn_id: str = "google_cloud_default",
        delegate_to: str = None,
    ) -> None:
        super().__init__(gcp_conn_id, delegate_to)
        self.api_version = api_version
        self.num_retries = self._get_field("num_retries", 5)  # type: int

    def get_conn(self):
        """
        Retrieves connection to Google Compute Engine.

        :return: Google Compute Engine services object
        :rtype: dict
        """
        if not self._conn:
            http_authorized = self._authorize()
            self._conn = build(
                "compute", self.api_version, http=http_authorized, cache_discovery=False
            )
        return self._conn

    @GoogleCloudBaseHook.fallback_to_default_project_id
    def start_instance(
        self, zone: str, resource_id: str, project_id: str = None
    ) -> None:
        """
        Starts an existing instance defined by project_id, zone and resource_id.
        Must be called with keyword arguments rather than positional.

        :param zone: Google Cloud Platform zone where the instance exists
        :type zone: str
        :param resource_id: Name of the Compute Engine instance resource
        :type resource_id: str
        :param project_id: Optional, Google Cloud Platform project ID where the
            Compute Engine Instance exists. If set to None or missing,
            the default project_id from the GCP connection is used.
        :type project_id: str
        :return: None
        """
        assert project_id is not None
        response = (
            self.get_conn()
            .instances()
            .start(  # pylint: disable=no-member
                project=project_id, zone=zone, instance=resource_id
            )
            .execute(num_retries=self.num_retries)
        )
        try:
            operation_name = response["name"]
        except KeyError:
            raise AirflowException(
                "Wrong response '{}' returned - it should contain "
                "'name' field".format(response)
            )
        self._wait_for_operation_to_complete(
            project_id=project_id, operation_name=operation_name, zone=zone
        )
