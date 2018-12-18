from .validation import (
    _validate_type_of_each_elements,
    _validate_disjoint,
)


class Group:
    '''Base class of EditGroup and SpanGroup'''

    def __init__(self, objs):
        '''
        Args:
            objs: list of Edits or Spans.
            target_type: Edit or Span.

        e.g.
            1. Group(edits)
            2. Group(spans)
        '''
        _validate_type_of_each_elements(objs)
        objs = sorted(objs, key=lambda e: e.end)
        _validate_disjoint(objs)
        self._objs = objs

    def __getitem__(self, value):
        return self._objs[value]

    def __len__(self):
        return len(self._objs)

    def __eq__(self, other):
        if len(other) != len(self._objs):
            return False
        for i in range(len(self._objs)):
            if other[i] != self._objs[i]:
                return False
        return True
