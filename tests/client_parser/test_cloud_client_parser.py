# -*- coding: utf-8 -*-
from unittest import TestCase, mock

from airflow_munchkin.client_parser import cloud_client_parser
from airflow_munchkin.client_parser.docstring_parser import SectionBrick
from airflow_munchkin.client_parser.docstring_parser.bricks import FieldBrick, TypeBrick
from airflow_munchkin.client_parser.infos import (
    PathInfo,
    ActionInfo,
    ParameterInfo,
    ClientInfo,
)


class CloudRedisClient:
    def __init__(self):
        """Constructor"""

    @classmethod
    def location_path(cls, project, location):
        """Return a fully-qualified location string."""

    def list_instances(  # pylint: disable=too-many-arguments
        self, parent, page_size=None, retry=None, timeout=None, metadata=None
    ):
        """DOCSTRING"""

    def get_instance(  # pylint: disable=too-many-arguments, unused-argument, no-self-use
        self, parent, insstance, page_size=None, retry=None, timeout=None, metadata=None
    ):
        return None


class TestParsePathMethod(TestCase):
    def test_should_parse_location(self):
        target_fn = CloudRedisClient.location_path
        result = cloud_client_parser.parse_path_method("location_path", target_fn)
        self.assertEqual(
            PathInfo(name="location_path", args=["project", "location"]), result
        )


class TestParseActionMethod(TestCase):
    parse_docstring_return_value = [
        SectionBrick(kind="Text", body=["TEXT1"]),
        SectionBrick(
            kind="Args",
            body=[
                FieldBrick(
                    name="parent",
                    type_brick=TypeBrick(kind="str", indexes=[]),
                    desc=[SectionBrick(kind="Text", body=["TEXT2"])],
                ),
                FieldBrick(
                    name="instance_id",
                    type_brick=TypeBrick(kind="str", indexes=[]),
                    desc=[SectionBrick(kind="Text", body=["TEXT3"])],
                ),
            ],
        ),
        SectionBrick(
            kind="Returns",
            body=[
                FieldBrick(
                    name="",
                    type_brick=None,
                    desc=[
                        SectionBrick(
                            kind="Text",
                            body=[
                                "A :class:`~google.cloud.redis_v1.types._OperationFuture` instance."
                            ],
                        )
                    ],
                )
            ],
        ),
    ]

    @mock.patch("airflow_munchkin.client_parser.cloud_client_parser.docstring_parser")
    def test_should_parse_redis_update_instance(self, mock_docstring_parser):
        mock_docstring_parser.parse_docstring.return_value = (
            self.parse_docstring_return_value
        )
        target_fn = CloudRedisClient.list_instances
        result = cloud_client_parser.parse_action_method("update_instance", target_fn)
        mock_docstring_parser.parse_docstring.assert_called_once_with("DOCSTRING")
        self.assertEqual(
            ActionInfo(
                name="update_instance",
                desc=["TEXT1"],
                args={
                    "parent": ParameterInfo(
                        name="parent",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=["TEXT2"],
                    ),
                    "instance_id": ParameterInfo(
                        name="instance_id",
                        kind=TypeBrick(kind="str", indexes=[]),
                        desc=["TEXT3"],
                    ),
                },
                return_kind=None,
                return_desc=[
                    "A :class:`~google.cloud.redis_v1.types._OperationFuture` instance."
                ],
            ),
            result,
        )

    @mock.patch("airflow_munchkin.client_parser.cloud_client_parser.docstring_parser")
    def test_should_parse_redis_get_instance_with_no_docstring(
        self, mock_docstring_parser
    ):
        mock_docstring_parser.parse_docstring.return_value = (
            self.parse_docstring_return_value
        )
        target_fn = CloudRedisClient.get_instance
        result = cloud_client_parser.parse_action_method("get_instance", target_fn)
        mock_docstring_parser.parse_docstring.assert_called_once_with(
            "None # TODO: Fill missing value"
        )
        self.assertIsNotNone(result)


class TestParseClient(TestCase):
    @mock.patch(
        "airflow_munchkin.client_parser.cloud_client_parser.parse_path_method",
        return_value="PATH_METHOD_INFO",
    )
    @mock.patch(
        "airflow_munchkin.client_parser.cloud_client_parser.parse_action_method",
        return_value="ACTION_METHOD_INFO",
    )
    @mock.patch(
        "airflow_munchkin.client_parser.cloud_client_parser.load_class",
        return_value=CloudRedisClient,
    )
    def test_should_parse_client(
        self, mock_load_class, mock_parse_action_method, mock_parse_path_method
    ):
        result = cloud_client_parser.parse_client("TEST_CLASS")

        mock_load_class.assert_called_once_with("TEST_CLASS")
        mock_parse_path_method.assert_any_call(
            "location_path", CloudRedisClient.location_path
        )
        mock_parse_action_method.assert_any_call("__init__", CloudRedisClient.__init__)
        self.assertEqual(
            ClientInfo(
                ctor_method="ACTION_METHOD_INFO",
                path_methods={"location_path": "PATH_METHOD_INFO"},
                action_methods={
                    "get_instance": "ACTION_METHOD_INFO",
                    "list_instances": "ACTION_METHOD_INFO",
                },
            ),
            result,
        )
