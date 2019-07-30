# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

from airflow_munchkin.block_renderer import jinja_filters


class TestWrapText(TestCase):
    def test_wrap_text_should_wrap_simple_long_text(self):
        input_text = [
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos magni inventore rem "
            "accusamus asperiores ipsam assumenda harum iure ullam error iste est ea id quasi voluptas.",
            "Dicta sint officiis, sunt, tempore blanditiis non quam! Aspernatur ipsa eius enim velit ",
            "necessitatibus, placeat a explicabo voluptate maiores voluptatibus, quasi labore odio ",
            "blanditiis veniam dolor tempore ducimus reprehenderit alias sapiente dolores consectetur.",
        ]
        output_text = textwrap.dedent(
            """
            Lorem ipsum dolor sit amet, consectetur adipisicing elit.
            Dignissimos magni inventore rem accusamus asperiores ipsam
            assumenda harum iure ullam error iste est ea id quasi
            voluptas.

            Dicta sint officiis, sunt, tempore blanditiis non quam!
            Aspernatur ipsa eius enim velit

            necessitatibus, placeat a explicabo voluptate maiores
            voluptatibus, quasi labore odio

            blanditiis veniam dolor tempore ducimus reprehenderit alias
            sapiente dolores consectetur.
            """
        ).strip()
        self.assertEqual(
            output_text, jinja_filters.wrap_text(input_text, 60, deindent_first=False)
        )

    def test_wrap_text_should_wrap_text_with_list(self):
        input_text = [
            "Required. Mask of fields to update. At least one path must be supplied in "
            "this field. The elements of the repeated paths field may only include these "
            "fields from ``Instance``:",
            "-  ``displayName``\n-  ``labels``\n-  ``memorySizeGb``\n-  ``redisConfig``",
            "If a dict is provided, it must be of the same form as the protobuf message "
            ":class:`~google.cloud.redis_v1.types.FieldMask`",
        ]
        output_text = textwrap.dedent(
            """
            Required. Mask of fields to update. At least one path must
            be supplied in this field. The elements of the repeated
            paths field may only include these fields from ``Instance``:

            -  ``displayName``
            -  ``labels``
            -  ``memorySizeGb``
            -
            ``redisConfig``

            If a dict is provided, it must be of the same form as the
            protobuf message
            :class:`~google.cloud.redis_v1.types.FieldMask`
            """
        ).strip()
        self.assertEqual(
            output_text, jinja_filters.wrap_text(input_text, 60, deindent_first=False)
        )


class TestToClassName(TestCase):
    def test_to_class_name(self):
        self.assertEqual("cat", jinja_filters.to_class_name("awesome.cat"))


class TestToPackageName(TestCase):
    def test_to_package_name(self):
        self.assertEqual("awesome", jinja_filters.to_package_name("awesome.cat"))
