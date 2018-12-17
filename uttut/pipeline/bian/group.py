from typing import List, Union

from .edit import Edit
from .span import Span

from .validation import (
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class Group:

    def __init__(
            self,
            objs: Union[List[Edit], List[Span]],
            target_type: Union[Edit, Span],
        ):
        _validate_type_of_each_elements(objs, target_type)
        objs = sorted(objs, key=lambda e: e.end)
        _validate_disjoint(objs)
        self._objs = objs

    def __getitem__(self, value):
        return self._objs[value]

    def __len__(self):
        return len(self._objs)


class EditGroup(Group):

    def __init__(self, edits: List[Edit]):
        super().__init__(objs=edits, target_type=Edit)


class SpanGroup(Group):

    def __init__(self, spans: List[Edit]):
        super().__init__(objs=spans, target_type=Span)
