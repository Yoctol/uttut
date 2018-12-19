from abc import ABC, abstractmethod
from typing import List, Union, Tuple
import warnings

from .validation import (
    _validate_start_end,
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class Edit(ABC):
    '''Represents an edit to a Sequence such as a string or a list

    A sequence is a collection of objects that can be indexed in a linear fashion. E.g. a string

    A edit to a sequence is a replacement of a continuous range of the sequence with the elements
    of the replacement sequence.

    E.g.
    The transformation from "" to "abc": Edit(0, 0, "abc")
    The transformation from "abc" to "aBc": Edit(1, 2, "B")
    The transformation from "aBc" to "aBcdef": Edit(3, 3, "def")
    The transformation from "aBcdef" to "": Edit(0, 6, "")
    Note that insertion at position i is represented as Edit(i, i, ...)
    ("Insertion at i" means that the original i-th element is moved to the right;
     similar to Python's list.insert)

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
        replacement (obj): the replacement
        annotation (str, optional): an annotation for this edit
    '''

    def __init__(
            self,
            start: int,
            end: int,
            replacement,
            annotation: str = None,
        ):
        _validate_start_end(start, end)
        self.start, self.end = start, end
        self.replacement = replacement
        self.annotation = annotation

    def __eq__(self, other):
        same_start = other.start == self.start
        same_end = other.end == self.end
        same_replacements = other.replacement == self.replacement
        return same_start and same_end and same_replacements

    def __str__(self):
        return f"({self.start}, {self.end}) => '{self.replacement}'"

    @abstractmethod
    def __repr__(self):
        pass


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


class EditGroup:

    def __init__(self):
        self._edits = set()
        self._is_done = False

    def add(self, start: int, end: int, replacement: Union[str, List[str]], annotation=None):
        if isinstance(replacement, str):
            edit = StrEdit(start=start, end=end, replacement=replacement, annotation=annotation)
        elif isinstance(replacement, list):
            edit = LstEdit(start=start, end=end, replacement=replacement, annotation=annotation)
        else:
            raise TypeError('replacement should be string or list.')
        self._edits.add(edit)

    def done(self):
        if len(self._edits) == 0:
            warnings.warn("EditGroup is empty")
            self._edits = list(self._edits)
        else:
            _validate_type_of_each_elements(list(self._edits))
            self._edits = sorted(self._edits, key=lambda e: e.end)  # set -> list
            _validate_disjoint(self._edits)
        self._is_done = True

    @classmethod
    def add_all(cls, edits: List[Tuple[int, int, Union[str, list]]]):
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
        return f"{list(self._edits)[0].__class__.__name__}Group"
