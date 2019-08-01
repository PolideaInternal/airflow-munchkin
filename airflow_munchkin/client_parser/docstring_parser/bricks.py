# -*- coding: utf-8 -*-
from typing import NamedTuple, List, Union, Optional, Any


class TypeBrick(NamedTuple):
    kind: str
    # Should be List[SectionBrick], but recursive types is not supported in mypy:
    # Issue: https://github.com/python/mypy/issues/731
    indexes: List[Any] = []

    def __str__(self) -> str:
        return self.long_form

    @property
    def name(self) -> str:
        _, _, name = self.kind.rpartition(".")
        return name

    @property
    def module(self) -> str:
        module, _, _ = self.kind.rpartition(".")
        return module

    @property
    def long_form(self) -> str:
        if self.indexes:
            indexes_str = ", ".join([element.long_form for element in self.indexes])
            return f"{self.kind}[{indexes_str}]"
        return self.kind

    @property
    def short_form(self) -> str:
        if self.indexes:
            indexes_str = ", ".join([element.short_form for element in self.indexes])
            return f"{self.name}[{indexes_str}]"
        return self.name

    @property
    def is_optional(self) -> bool:
        return self.kind == "Optional" or self.kind == "typing.Optional"

    @property
    def is_union(self) -> bool:
        return self.kind == "Union" or self.kind == "typing.Union"


class FieldBrick(NamedTuple):
    name: str
    type_brick: Optional[TypeBrick]
    # Should be List[SectionBrick], but recursive types is not supported in mypy:
    # Issue: https://github.com/python/mypy/issues/731
    desc: List[Any]  # type: ignore


class SectionBrick(NamedTuple):
    kind: str
    body: Union[List[str], List[FieldBrick]]  # type: ignore
