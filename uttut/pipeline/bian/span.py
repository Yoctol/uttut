from typing import List

from .validation import (
    validate_start_end,
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class Span:
    '''Integer offsets (start_i, end_i) of a sequence

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
    '''

    def __init__(
            self,
            start: int,
            end: int,
        ):
        self.start, self.end = validate_start_end(start, end)

    def __eq__(self, other):
        if not isinstance(other, Span):
            return False
        same_start = other.start == self.start
        same_end = other.end == self.end
        return same_start and same_end

    def __str__(self):
        return f"({self.start}, {self.end})"

    def __repr__(self):
        return f"Span({self.start}, {self.end})"


class SpanGroup:

    def __init__(self, spans: List[Span]):
        _validate_type_of_each_elements(spans, Span)
        spans = sorted(spans, key=lambda e: e.end)
        _validate_disjoint(spans)
        self._spans = spans

    @property
    def spans(self):
        return self._spans
