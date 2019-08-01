# -*- coding: utf-8 -*-
import unittest

from parameterized import parameterized

from airflow_munchkin.client_parser.docstring_parser import typehint_parser
from airflow_munchkin.client_parser.docstring_parser.bricks import TypeBrick


class TestTypeHintParser(unittest.TestCase):
    def test_should_parse_primitives(self):
        self.assertEqual(
            TypeBrick(kind="str", indexes=[]), typehint_parser.parse_typehint("str")
        )

    def test_should_parse_class(self):
        self.assertEqual(
            TypeBrick(kind="airflow_munchkin.typehint_parser", indexes=[]),
            typehint_parser.parse_typehint("airflow_munchkin.typehint_parser"),
        )

    def test_should_parse_list(self):
        self.assertEqual(
            TypeBrick(kind="List", indexes=[TypeBrick(kind="str", indexes=[])]),
            typehint_parser.parse_typehint("List[str]"),
        )

    def test_should_parse_dict(self):
        self.assertEqual(
            TypeBrick(
                kind="Dict",
                indexes=[
                    TypeBrick(kind="str", indexes=[]),
                    TypeBrick(kind="str", indexes=[]),
                ],
            ),
            typehint_parser.parse_typehint("Dict[str, str]"),
        )

    def test_should_fix_incorrect_type(self):
        self.assertEqual(
            TypeBrick(
                kind="Dict",
                indexes=[
                    TypeBrick(kind="str", indexes=[]),
                    TypeBrick(kind="float", indexes=[]),
                ],
            ),
            typehint_parser.parse_typehint("dict[str -> float]"),
        )

    def test_should_refinement_dict(self):
        self.assertEqual(
            TypeBrick(kind="Dict", indexes=[]), typehint_parser.parse_typehint("dict")
        )

    def test_should_refinement_nested_dict(self):
        self.assertEqual(
            TypeBrick(
                kind="Union",
                indexes=[
                    TypeBrick(
                        kind="Optional", indexes=[TypeBrick(kind="Dict", indexes=[])]
                    )
                ],
            ),
            typehint_parser.parse_typehint("Union[Optional[dict]]"),
        )

    @parameterized.expand(
        [
            (TypeBrick(kind="str", indexes=[]), "str"),
            (
                TypeBrick(
                    kind="Union",
                    indexes=[
                        TypeBrick(kind="Dict", indexes=[]),
                        TypeBrick(
                            kind="google.cloud.automl_v1beta1.types.BatchPredictInputConfig",
                            indexes=[],
                        ),
                    ],
                ),
                "Union[dict, ~google.cloud.automl_v1beta1.types.BatchPredictInputConfig]",
            ),
            (
                TypeBrick(
                    kind="Union",
                    indexes=[
                        TypeBrick(kind="Dict", indexes=[]),
                        TypeBrick(
                            kind="google.cloud.automl_v1beta1.types.BatchPredictOutputConfig",
                            indexes=[],
                        ),
                    ],
                ),
                "Union[dict, ~google.cloud.automl_v1beta1.types.BatchPredictOutputConfig]",
            ),
            (
                TypeBrick(
                    kind="Dict",
                    indexes=[
                        TypeBrick(kind="str", indexes=[]),
                        TypeBrick(kind="str", indexes=[]),
                    ],
                ),
                "Dict[str, str]",
            ),
            (
                TypeBrick(
                    kind="Optional",
                    indexes=[TypeBrick(kind="google.api_core.retry.Retry", indexes=[])],
                ),
                "Optional[google.api_core.retry.Retry]",
            ),
            (
                TypeBrick(
                    kind="Optional", indexes=[TypeBrick(kind="float", indexes=[])]
                ),
                "Optional[float]",
            ),
            (
                TypeBrick(
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
                "Optional[Sequence[Tuple[str, str]]]",
            ),
            (TypeBrick(kind="str", indexes=[]), "str"),
            (
                TypeBrick(
                    kind="Union",
                    indexes=[
                        TypeBrick(kind="Dict", indexes=[]),
                        TypeBrick(
                            kind="google.cloud.automl_v1beta1.types.ExamplePayload",
                            indexes=[],
                        ),
                    ],
                ),
                "Union[dict, ~google.cloud.automl_v1beta1.types.ExamplePayload]",
            ),
            (
                TypeBrick(
                    kind="Dict",
                    indexes=[
                        TypeBrick(kind="str", indexes=[]),
                        TypeBrick(kind="str", indexes=[]),
                    ],
                ),
                "Dict[str, str]",
            ),
            (
                TypeBrick(
                    kind="Optional",
                    indexes=[TypeBrick(kind="google.api_core.retry.Retry", indexes=[])],
                ),
                "Optional[google.api_core.retry.Retry]",
            ),
            (
                TypeBrick(
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
                "Optional[Sequence[Tuple[str, str]]]",
            ),
        ]
    )
    def test_real_cases(self, exptected_result, input_text):
        self.assertEqual(exptected_result, typehint_parser.parse_typehint(input_text))
