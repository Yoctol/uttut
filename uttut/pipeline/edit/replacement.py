from typing import List, Union
import warnings

from .base import Replacement, Group
from .validation import (
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class StrReplacement(Replacement):

    def __init__(
            self,
            start: int,
            end: int,
            new_value: str,
            annotation: str = None,
        ):
        if not isinstance(new_value, str):
            raise TypeError('StrReplacement needs a string type new_value.')
        super().__init__(start=start, end=end, new_value=new_value, annotation=annotation)

    def __eq__(self, other):
        if not isinstance(other, StrReplacement):
            return False
        return super().__eq__(other)

    def __repr__(self):
        output_repr = f"StrReplacement({self.start}, {self.end}, " \
            f"{self.new_value}, annotation={self.annotation})"
        return output_repr

    def __hash__(self):
        return hash(self.__repr__())


class LstReplacement(Replacement):

    def __init__(
            self,
            start: int,
            end: int,
            new_value: List[str],
            annotation: str = None,
        ):
        if not isinstance(new_value, list):
            raise TypeError('LstReplacement needs a list type new_value.')
        super().__init__(start=start, end=end, new_value=new_value, annotation=annotation)

    def __eq__(self, other):
        if not isinstance(other, LstReplacement):
            return False
        return super().__eq__(other)

    def __repr__(self):
        output_repr = f"LstReplacement({self.start}, {self.end}, " \
            f"{self.new_value}, annotation={self.annotation})"
        return output_repr

    def __hash__(self):
        return hash(self.__repr__())


class ReplacementGroup(Group):

    def __init__(self):
        self._replacements = set()
        super().__init__()

    def add(  # type: ignore
            self,
            start: int,
            end: int,
            new_value: Union[str, List[str]],
            annotation=None,
        ):
        replacement: Replacement
        if isinstance(new_value, str):
            replacement = StrReplacement(
                start=start,
                end=end,
                new_value=new_value,
                annotation=annotation,
            )
        elif isinstance(new_value, list):
            replacement = LstReplacement(
                start=start,
                end=end,
                new_value=new_value,
                annotation=annotation,
            )
        else:
            raise TypeError('new_value should be string or list.')
        self._replacements.add(replacement)

    def done(self):
        if len(self._replacements) == 0:
            self._replacements = list(self._replacements)
        else:
            _validate_type_of_each_elements(list(self._replacements))
            self._replacements = sorted(self._replacements, key=lambda e: e.end)  # set -> list
            self._replacements = sorted(self._replacements, key=lambda e: e.start)
            _validate_disjoint(self._replacements)
        self._is_done = True

    @classmethod
    def add_all(cls, replacements: List[tuple]) -> 'ReplacementGroup':  # type: ignore
        '''
        replacements = [
            (
                start: int,
                end: int,
                new_value: Union[str, list[str]],
                annotation: str, # optional
            ),
            ...
        ]
        '''
        replacement_group = cls()
        for replacement in replacements:
            if len(replacement) == 3:
                start, end, new_value = replacement
                replacement_group.add(start, end, new_value)
            elif len(replacement) == 4:
                start, end, new_value, annotation = replacement
                replacement_group.add(start, end, new_value, annotation)
            else:
                raise ValueError('Number of elements should = 3 or 4.')
        replacement_group.done()
        return replacement_group

    def is_empty(self):
        return len(self._replacements) == 0

    def __eq__(self, other):
        self._warn_not_done()
        if not isinstance(other, ReplacementGroup):
            return False
        same_length = len(other) == len(self._replacements)
        same_elements = set(other) == set(self._replacements)
        return same_length and same_elements

    def __getitem__(self, value):
        if not self._is_done:
            raise RuntimeError('Please call `done` first.')
        return self._replacements[value]

    def __len__(self):
        self._warn_not_done()
        return len(self._replacements)

    def _warn_not_done(self):
        if not self._is_done:
            warnings.warn('ReplacementGroup needs validation, please call `done`.')

    def __repr__(self):
        if self.is_empty():
            return f"EmptyReplacementGroup"
        return f"{list(self._replacements)[0].__class__.__name__}Group"
