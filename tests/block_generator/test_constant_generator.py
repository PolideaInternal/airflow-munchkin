# -*- coding: utf-8 -*-
from unittest import TestCase

from parameterized import parameterized

from airflow_munchkin.block_generator import constant_generator
from airflow_munchkin.block_generator.blocks import Constant
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class TestConstantGenerator(TestCase):
    @parameterized.expand(
        [
            (
                {"arg": None},
                [
                    Constant(
                        name="TEST_ARG",
                        value="None # TODO: Fill missing value",
                        kind=TypeBrick(kind="None"),
                    )
                ],
            ),
            (
                {"arg2": None},
                [
                    Constant(
                        name="TEST_ARG2",
                        value="None # TODO: Fill missing value",
                        kind=TypeBrick(kind="None"),
                    )
                ],
            ),
            (
                {"arg": None, "arg2": None},
                [
                    Constant(
                        name="TEST_ARG",
                        value="None # TODO: Fill missing value",
                        kind=TypeBrick(kind="None"),
                    ),
                    Constant(
                        name="TEST_ARG2",
                        value="None # TODO: Fill missing value",
                        kind=TypeBrick(kind="None"),
                    ),
                ],
            ),
            (
                {"arg3": TypeBrick(kind="Optional", indexes=[TypeBrick(kind="Dict")])},
                [
                    Constant(
                        name="TEST_ARG3",
                        value="None # TODO: Fill missing value",
                        kind=TypeBrick(kind="Dict"),
                    )
                ],
            ),
            (
                {"arg3": TypeBrick(kind="str")},
                [
                    Constant(
                        name="TEST_ARG3",
                        value="'test-arg3'",
                        kind=TypeBrick(kind="str"),
                    )
                ],
            ),
            (
                {"arg3": TypeBrick(kind="Optional", indexes=[TypeBrick(kind="str")])},
                [
                    Constant(
                        name="TEST_ARG3",
                        value="'test-arg3'",
                        kind=TypeBrick(kind="str"),
                    )
                ],
            ),
        ]
    )
    def test_parse_generate_for_node(self, current_input, expected_output):
        result = constant_generator.generate_constant_list(current_input)
        self.assertEqual(result, expected_output)
