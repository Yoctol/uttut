from typing import List

from .validation import _validate_start_end
from .utils import Group


class Span:
    '''Integer offsets (start_i, end_i) of a sequence

    Args:
        start (int): start index (inclusive)
        end (int): end index (exclusive)
    '''

    def __init__(self, start: int, end: int):
        _validate_start_end(start, end)
        self.start, self.end = start, end

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


class SpanGroup(Group):

    def __init__(self, spans: List[Span]):
        super().__init__(objs=spans)
        self._validate_contiguousness(self._objs)

    def _validate_contiguousness(self, sorted_spans):
        if sorted_spans[0].start != 0:
            raise ValueError('Spans should start from 0')
        for idx in range(len(sorted_spans) - 1):
            if sorted_spans[idx].end != sorted_spans[idx + 1].start:
                raise ValueError('Spans should be contiguous.')

    def __eq__(self, other):
        if not isinstance(other, SpanGroup):
            return False
        return super().__eq__(other)
