# -*- coding: utf-8 -*-
import textwrap
from unittest import TestCase

from airflow_munchkin.block_renderer import jinja_functions


class TestRstParam(TestCase):
    def test_rst_param_should_format_simple_case(self):
        text = []
        result = jinja_functions.rst_param(name="NAME", desc=text, width=110)
        self.assertEqual(":param NAME:", result)

    def test_rst_param_should_format_text(self):
        text = [
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, vero! Saepe eligendi quos "
            "dolore illo vel, illum omnis animi sequi laborum ipsam nobis obcaecati dolorum doloribus dicta "
            "enim. Adipisci aliquid minima, reiciendis dolorem consequatur optio suscipit iusto nostrum "
            "dolores. "
        ]
        result = jinja_functions.rst_param(name="NAME", desc=text, width=60)
        expected_result = textwrap.dedent(
            """
        :param NAME: Lorem ipsum dolor sit amet, consectetur
            adipisicing elit. Laboriosam, vero! Saepe eligendi quos
            dolore illo vel, illum omnis animi sequi laborum ipsam
            nobis obcaecati dolorum doloribus dicta enim. Adipisci
            aliquid minima, reiciendis dolorem consequatur optio
            suscipit iusto nostrum dolores.
        """
        ).strip()
        self.assertEqual(expected_result, result)

    def test_rst_param_should_format_text_with_multiple_paragraph(self):
        text = [
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, vero! Saepe eligendi quos "
            "dolore illo vel, illum omnis animi sequi laborum ipsam nobis obcaecati dolorum doloribus dicta "
            "enim. Adipisci aliquid minima, reiciendis dolorem consequatur optio suscipit iusto nostrum "
            "dolores. ",
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laboriosam, vero! Saepe eligendi quos "
            "dolore illo vel, illum omnis animi sequi laborum ipsam nobis obcaecati dolorum doloribus dicta "
            "enim. Adipisci aliquid minima, reiciendis dolorem consequatur optio suscipit iusto nostrum "
            "dolores. ",
        ]
        result = jinja_functions.rst_param(name="NAME", desc=text, width=60)
        expected_result = textwrap.dedent(
            """
        :param NAME: Lorem ipsum dolor sit amet, consectetur
            adipisicing elit. Laboriosam, vero! Saepe eligendi quos
            dolore illo vel, illum omnis animi sequi laborum ipsam
            nobis obcaecati dolorum doloribus dicta enim. Adipisci
            aliquid minima, reiciendis dolorem consequatur optio
            suscipit iusto nostrum dolores.

            Lorem ipsum dolor sit amet, consectetur adipisicing
            elit. Laboriosam, vero! Saepe eligendi quos dolore illo
            vel, illum omnis animi sequi laborum ipsam nobis
            obcaecati dolorum doloribus dicta enim. Adipisci aliquid
            minima, reiciendis dolorem consequatur optio suscipit
            iusto nostrum dolores.
        """
        ).strip()
        self.assertEqual(expected_result, result)
