from typing import List, Tuple

from .edit import EditGroup
from .span import SpanGroup
from uttut.pipeline.bian import str2str


def apply(
        input_lst: List[str],
        span_group: SpanGroup,
        edit_group: EditGroup,
    ) -> List[str]:

    _validate_compatibility(input_lst, span_group)

    # 1. apply span group (list -> str)
    output_str = ''.join(input_lst)

    # 2. apply edit group (str -> str)
    output_str = str2str.apply(output_str, edit_group)

    return output_str


def inverse(
        input_lst: List[str],
        span_group: SpanGroup,
        edit_group: EditGroup,
    ) -> Tuple[EditGroup, SpanGroup]:

    _validate_compatibility(input_lst, span_group)

    # inverse edit group only
    inverse_edit_group = EditGroup.add_all([])
    if not edit_group.is_empty():
        inverse_edit_group = str2str.inverse(''.join(input_lst), edit_group)

    return inverse_edit_group, span_group


def _validate_compatibility(input_lst: List[str], span_group: SpanGroup):
    if len(input_lst) != len(span_group):
        raise ValueError('Input list and span group have different length.')
    for i, (token, span) in enumerate(zip(input_lst, span_group)):
        if len(token) != span.end - span.start:
            raise ValueError(f"{i}-th element is not compatible.")
