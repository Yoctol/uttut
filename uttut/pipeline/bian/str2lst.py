from typing import List, Tuple

from .edit import EditGroup
from .span import SpanGroup
from uttut.pipeline.bian import str2str


def apply(
        input_str: str,
        edit_group: EditGroup,
        span_group: SpanGroup,
    ) -> List[str]:

    # 1. apply edits (str -> str)
    output_str = input_str
    if not edit_group.is_empty():
        output_str = str2str.apply(input_str, edit_group)

    # 2. apply spans (str -> list)
    output_lst = [''] * len(span_group)
    for i, span in enumerate(span_group):
        output_lst[i] = output_str[span.start: span.end]

    return output_lst


def inverse(
        input_str: str,
        edit_group: EditGroup,
        span_group: SpanGroup,
    ) -> Tuple[EditGroup, SpanGroup]:

    # inverse edit group only
    inverse_edit_group = EditGroup.add_all([])
    if not edit_group.is_empty():
        inverse_edit_group = str2str.inverse(input_str, edit_group)

    return inverse_edit_group, span_group


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
