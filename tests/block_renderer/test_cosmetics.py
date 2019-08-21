# -*- coding: utf-8 -*-
from pathlib import Path
from unittest import TestCase, mock

from airflow_munchkin.block_renderer import cosmetics


class TestRemoveUnusedImports(TestCase):
    @mock.patch("airflow_munchkin.block_renderer.cosmetics.fix_file")
    def test_remove_unused_imports(self, mock_fix_file):  # pylint: disable=no-self-use
        cosmetics.remove_unused_imports("PATH")
        mock_fix_file.assert_called_once_with(
            "PATH", args=mock.ANY, standard_out=mock.ANY
        )


class TestFormatWithBlack(TestCase):
    @mock.patch("airflow_munchkin.block_renderer.cosmetics.black")
    def test_format_with_black(self, mock_black):  # pylint: disable=no-self-use
        cosmetics.format_with_black("PATH")
        mock_black.format_file_in_place.assert_called_once_with(
            Path("PATH"), fast=False, mode=mock.ANY, write_back=mock.ANY
        )


class TestSortImports(TestCase):
    @mock.patch("airflow_munchkin.block_renderer.cosmetics.SortImports")
    def test_sort_imports(self, mock_sort_imports):  # pylint: disable=no-self-use
        cosmetics.sort_imports("PATH")
        mock_sort_imports.assert_called_once_with("PATH")
