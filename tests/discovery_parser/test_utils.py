# -*- coding: utf-8 -*-
from unittest import TestCase
from parameterized import parameterized


from airflow_munchkin.discovery_parser.utils import (
    camel_to_snake,
    capitalize_first_letter,
    split_on_uppers,
    resolve_package_name,
)


class TestUtils(TestCase):
    @parameterized.expand(
        [
            ("small_snake", "SmallSnake"),
            ("snake_snake100", "SnakeSnake100"),
            ("snake_snake", "snake_snake"),
        ]
    )
    def test_camel_to_snake(self, expected, content):
        self.assertEqual(expected, camel_to_snake(content))

    @parameterized.expand([("Big", "big"), ("42magic", "42magic"), ("Big", "Big")])
    def test_capitalize_first_letter(self, expected, content):
        self.assertEqual(expected, capitalize_first_letter(content))

    @parameterized.expand(
        [
            (["Big", "Thing"], "BigThing"),
            (["do-nothing"], "do-nothing"),
            (["Big"], "Big"),
        ]
    )
    def test_split_on_uppers(self, expected, content):
        self.assertEqual(expected, split_on_uppers(content))

    @parameterized.expand(
        [
            ("package_name", "PackageName"),
            ("super_package", "super_package"),
            ("package", "package"),
        ]
    )
    def test_resolve_package_name(self, expected, content):
        self.assertEqual(expected, resolve_package_name(content))
