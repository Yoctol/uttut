from typing import List, Union
import warnings

from .base import Edit, Group
from .validation import (
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class StrEdit(Edit):

    def __init__(
            self,
            start: int,
            end: int,
            replacement: str,
            annotation: str = None,
        ):
        if not isinstance(replacement, str):
            raise TypeError('StrEdit needs string replacement.')
        super().__init__(start=start, end=end, replacement=replacement, annotation=annotation)

    def __eq__(self, other):
        if not isinstance(other, StrEdit):
            return False
        return super().__eq__(other)

    def __repr__(self):
        output_repr = f"StrEdit({self.start}, {self.end}, " \
            f"{self.replacement}, annotation={self.annotation})"
        return output_repr

    def __hash__(self):
        return hash(self.__repr__())


class LstEdit(Edit):

    def __init__(
            self,
            start: int,
            end: int,
            replacement: List[str],
            annotation: str = None,
        ):
        if not isinstance(replacement, list):
            raise TypeError('LstEdit needs list replacement.')
        super().__init__(start=start, end=end, replacement=replacement, annotation=annotation)

    def __eq__(self, other):
        if not isinstance(other, LstEdit):
            return False
        return super().__eq__(other)

    def __repr__(self):
        output_repr = f"LstEdit({self.start}, {self.end}, " \
            f"{self.replacement}, annotation={self.annotation})"
        return output_repr

    def __hash__(self):
        return hash(self.__repr__())


class EditGroup(Group):

    def __init__(self):
        self._edits = set()
        super().__init__()

    def add(  # type: ignore
            self,
            start: int,
            end: int,
            replacement: Union[str, List[str]],
            annotation=None,
        ):
        edit: Edit
        if isinstance(replacement, str):
            edit = StrEdit(start=start, end=end, replacement=replacement, annotation=annotation)
        elif isinstance(replacement, list):
            edit = LstEdit(start=start, end=end, replacement=replacement, annotation=annotation)
        else:
            raise TypeError('replacement should be string or list.')
        self._edits.add(edit)

    def done(self):
        if len(self._edits) == 0:
            self._edits = list(self._edits)
        else:
            _validate_type_of_each_elements(list(self._edits))
            self._edits = sorted(self._edits, key=lambda e: e.end)  # set -> list
            self._edits = sorted(self._edits, key=lambda e: e.start)
            _validate_disjoint(self._edits)
        self._is_done = True

    @classmethod
    def add_all(cls, edits: List[tuple]) -> 'EditGroup':  # type: ignore
        '''
        edits = [
            (
                start: int,
                end: int,
                replacement: Union[str, list[str]],
                annotation: str, # optional
            ),
            ...
        ]
        '''
        edit_group = cls()
        for edit in edits:
            if len(edit) == 3:
                start, end, replacement = edit
                edit_group.add(start, end, replacement)
            elif len(edit) == 4:
                start, end, replacement, annotation = edit
                edit_group.add(start, end, replacement, annotation)
            else:
                raise ValueError('Number of elements should = 3 or 4.')
        edit_group.done()
        return edit_group

    def is_empty(self):
        return len(self._edits) == 0

    def __eq__(self, other):
        self._warn_not_done()
        if not isinstance(other, EditGroup):
            return False
        same_length = len(other) == len(self._edits)
        same_elements = set(other) == set(self._edits)
        return same_length and same_elements

    def __getitem__(self, value):
        if not self._is_done:
            raise RuntimeError('Please call `done` first.')
        return self._edits[value]

    def __len__(self):
        self._warn_not_done()
        return len(self._edits)

    def _warn_not_done(self):
        if not self._is_done:
            warnings.warn('EditGroup needs validation, please call `done`.')

    def __repr__(self):
        if self.is_empty():
            return f"EmptyEditGroup"
        return f"{list(self._edits)[0].__class__.__name__}Group"
