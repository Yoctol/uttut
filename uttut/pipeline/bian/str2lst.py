from typing import List

from .edit import EditGroup
from .span import SpanGroup


def apply(input_str: str, span_group: SpanGroup) -> List[str]:

    _validate_compatibility(input_str, span_group)

    output_lst = [''] * len(span_group)
    for i, span in enumerate(span_group):
        output_lst[i] = input_str[span.start: span.end]

    return output_lst


def _validate_compatibility(input_str: str, span_group: SpanGroup):
    if len(input_str) != span_group[-1].end:
        raise ValueError('Input list and span group is not compatible.')


def gen_span_group(input_str: str, tokens: List[str]) -> SpanGroup:
    '''Compare string and tokens then generate SpanGroup'''

    if input_str != ''.join(tokens):
        raise ValueError('input_str and tokens are not compatible')

    shift = 0
    span_group = SpanGroup()
    for token in tokens:
        start = input_str.find(token, shift)
        end = start + len(token)
        span_group.add(start, end)
        shift = end
    span_group.done()
    assert len(span_group) == len(tokens)
    return span_group


def gen_edit_group(input_str: str, tokens: List[str]) -> EditGroup:
    '''Compare string and tokens then generate EditGroup'''

    shift = 0
    edit_group = EditGroup()
    for token in tokens:
        start = input_str.find(token, shift)
        if start == -1:
            ValueError('input_str and tokens are not compatible')
        if input_str[shift: start] != '':
            edit_group.add(shift, start, '')
        shift = start + len(token)
    edit_group.done()
    return edit_group
