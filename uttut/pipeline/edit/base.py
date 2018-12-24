from collections.abc import Sequence
from abc import ABC, abstractmethod, abstractclassmethod

from .validation import _validate_start_end


class Replacement(ABC):
    '''Represents an edit to a Sequence such as a string or a list

    A sequence is a collection of objects that can be indexed in a linear fashion. E.g. a string

    A `Replacement` stores the data for substitution of values in a sequence.
    It represents the replacing a continuous slice of the sequence with the items of `new_value`.
    (The semantics are similar to Python's built-in slice assignment feature
     https://docs.python.org/3/reference/simple_stmts.html#assignment-statements ,
     but more restrictive in that negative integers are not allowed for `start` and `end`.)


    E.g.
    The transformation from "" to "abc": Replacement(0, 0, "abc")
    The transformation from "abc" to "aBc": Replacement(1, 2, "B")
    The transformation from "aBc" to "aBcdef": Replacement(3, 3, "def")
    The transformation from "aBcdef" to "": Replacement(0, 6, "")
    Note that insertion at position i is represented as Replacement(i, i, ...)
    ("Insertion at i" means that the original i-th element is moved to the right;
     similar to Python's list.insert)

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
        new_value (obj): the new subsequence
        annotation (str, optional): an annotation for this replacement
    '''

    def __init__(
            self,
            start: int,
            end: int,
            new_value,
            annotation: str = None,
        ):
        _validate_start_end(start, end)
        self.start, self.end = start, end
        self.new_value = new_value
        self.annotation = annotation

    def __eq__(self, other):
        same_start = other.start == self.start
        same_end = other.end == self.end
        same_new_values = other.new_value == self.new_value
        return same_start and same_end and same_new_values

    def __str__(self):
        return f"({self.start}, {self.end}) => '{self.new_value}'"

    @abstractmethod
    def __repr__(self):
        pass


class Group(Sequence):

    def __init__(self):
        self._is_done = False

    @abstractmethod
    def add(self):
        pass

    @abstractclassmethod
    def add_all(cls):
        pass

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def _warn_not_done(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
