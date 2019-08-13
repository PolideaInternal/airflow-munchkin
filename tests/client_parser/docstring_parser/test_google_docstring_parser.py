# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

from airflow_munchkin.client_parser.docstring_parser import (
    GoogleDocstringParser,
    SectionBrick,
)
from airflow_munchkin.client_parser.docstring_parser.bricks import FieldBrick, TypeBrick


class TestGoogleDocstringParser(TestCase):
    def test_should_parse_description(self):
        docstring = textwrap.dedent(
            """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, vero! Saepe eligendi quos
        dolore illo vel, illum omnis animi sequi laborum ipsam nobis obcaecati dolorum doloribus dicta enim.
        Adipisci aliquid minima, reiciendis dolorem consequatur optio suscipit iusto nostrum dolores,
        """
        )
        sections = GoogleDocstringParser(docstring).sections()
        self.assertEqual(
            [
                SectionBrick(
                    kind="Text",
                    body=[
                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, vero! Saepe "
                        "eligendi quos dolore illo vel, illum omnis animi sequi laborum ipsam nobis "
                        "obcaecati dolorum doloribus dicta enim. Adipisci aliquid minima, reiciendis "
                        "dolorem consequatur optio suscipit iusto nostrum dolores,"
                    ],
                )
            ],
            sections,
        )

    def test_should_skip_unknown_section(self):
        docstring = textwrap.dedent(
            """
        Gets the details of a specific Redis instance.

        Example:
            >>> from google.cloud import redis_v1beta1
            >>>
            >>> client = redis_v1beta1.CloudRedisClient()
            >>>
            >>> name = client.instance_path('[PROJECT]', '[LOCATION]', '[INSTANCE]')
            >>>
            >>> response = client.get_instance(name)
        """
        )
        sections = GoogleDocstringParser(docstring).sections()
        self.assertEqual(
            [
                SectionBrick(
                    kind="Text", body=["Gets the details of a specific Redis instance."]
                )
            ],
            sections,
        )

    def test_should_skip_parse_args(self):
        docstring = textwrap.dedent(
            """
        Gets the details of a specific Redis instance.

        Args:
            name (str): Required. Redis instance resource name using the form:
                ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
                where ``location_id`` refers to a GCP region
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        """
        )
        sections = GoogleDocstringParser(docstring).sections()
        self.assertEqual(
            [
                SectionBrick(
                    kind="Text", body=["Gets the details of a specific Redis instance."]
                ),
                SectionBrick(
                    kind="Args",
                    body=[
                        FieldBrick(
                            name="name",
                            type_brick=TypeBrick(kind="str", indexes=[]),
                            desc=[
                                SectionBrick(
                                    kind="Text",
                                    body=[
                                        "Required. Redis instance resource name using the form: "
                                        "``projects/{project_id}/locations/{location_id}/instances/"
                                        "{instance_id}`` where ``location_id`` refers to a GCP region"
                                    ],
                                )
                            ],
                        ),
                        FieldBrick(
                            name="retry",
                            type_brick=TypeBrick(
                                kind="Optional",
                                indexes=[
                                    TypeBrick(
                                        kind="google.api_core.retry.Retry", indexes=[]
                                    )
                                ],
                            ),
                            desc=[
                                SectionBrick(
                                    kind="Text",
                                    body=[
                                        "A retry object used to retry requests. If ``None`` is specified, "
                                        "requests will not be retried."
                                    ],
                                )
                            ],
                        ),
                        FieldBrick(
                            name="timeout",
                            type_brick=TypeBrick(
                                kind="Optional",
                                indexes=[TypeBrick(kind="float", indexes=[])],
                            ),
                            desc=[
                                SectionBrick(
                                    kind="Text",
                                    body=[
                                        "The amount of time, in seconds, to wait for the request to "
                                        "complete. Note that if ``retry`` is specified, the timeout applies "
                                        "to each individual attempt."
                                    ],
                                )
                            ],
                        ),
                        FieldBrick(
                            name="metadata",
                            type_brick=TypeBrick(
                                kind="Optional",
                                indexes=[
                                    TypeBrick(
                                        kind="Sequence",
                                        indexes=[
                                            TypeBrick(
                                                kind="Tuple",
                                                indexes=[
                                                    TypeBrick(kind="str", indexes=[]),
                                                    TypeBrick(kind="str", indexes=[]),
                                                ],
                                            )
                                        ],
                                    )
                                ],
                            ),
                            desc=[
                                SectionBrick(
                                    kind="Text",
                                    body=[
                                        "Additional metadata that is provided to the method."
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
            ],
            sections,
        )

    def test_should_skip_parse_returns(self):
        docstring = textwrap.dedent(
            """
        Gets the details of a specific Redis instance.

        Returns:
            A :class:`~google.cloud.redis_v1beta1.types.Instance` instance.
        """
        )
        sections = GoogleDocstringParser(docstring).sections()
        self.assertEqual(
            [
                SectionBrick(
                    kind="Text", body=["Gets the details of a specific Redis instance."]
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
                                        "A :class:`~google.cloud.redis_v1beta1.types.Instance` instance."
                                    ],
                                )
                            ],
                        )
                    ],
                ),
            ],
            sections,
        )
