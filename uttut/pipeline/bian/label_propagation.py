from typing import List, Callable, Sequence
from collections import Counter

from .edit import EditGroup
from .span import SpanGroup


def propagate_by_edit_group(
        labels: List[int],
        edit_group: EditGroup,
        reduce_func: Callable[[List[int]], int] = None,
    ) -> List[int]:
    '''Map the labels[fstart_i: fend_i] to output_labels[rstart_i: rend_i]
    Note that the length of edit_group should be the same as that of backward_edit_group.
    Map the reduced label in [forward_edit[i].start, forward_edit[i].end)
    to output list
    Args:
        labels (list of ints)
        edit_group (EditGroup)
        reduce_func (Callable): a function that return an integer given a list of integers.
    Return:
        labels (list of ints)
    '''
    if reduce_func is None:
        reduce_func = _get_most_common_label

    output_len = _compute_output_length(labels, edit_group)
    output_labels = [0] * output_len

    i_start = 0
    o_start = 0

    for edit in edit_group:
        # before edit
        fixed_len = edit.start - i_start
        output_labels[o_start: o_start + fixed_len] = labels[i_start: edit.start]
        o_start += fixed_len

        # edit
        label = reduce_func(labels[edit.start: edit.end])
        expand_size = len(edit.replacement)
        output_labels[o_start: o_start + expand_size] = [label] * expand_size

        i_start = edit.end
        o_start += expand_size

    # final
    output_labels[o_start:] = labels[i_start:]
    return output_labels


def _get_most_common_label(labels: List[int]):
    if len(labels) == 0:
        return 0
    counter = Counter(labels)
    return counter.most_common(1)[0][0]


def _compute_output_length(
        input_seq: Sequence,
        edit_group: EditGroup,
    ) -> int:
    # use cases: str -> str or list -> list
    len_iters = len(input_seq)
    offset = 0
    for edit in edit_group:
        after = len(edit.replacement)
        before = edit.end - edit.start
        offset += after - before

    return len_iters + offset


def reduce_by_span_group(
        labels: List[int],
        span_group: SpanGroup,
        reduce_func: Callable[[List[int]], int] = None,
    ) -> List[int]:
    # use case: string -> list

    if reduce_func is None:
        reduce_func = _get_most_common_label

    if len(labels) != span_group[-1].end:
        raise ValueError('labels and span_group are not compatible.')

    output_len = len(span_group)
    output_labels = [0] * output_len

    for i, span in enumerate(span_group):
        label = reduce_func(labels[span.start: span.end])
        output_labels[i] = label

    return output_labels


def expand_by_span_group(
        labels: List[int],
        span_group: SpanGroup,
    ) -> List[int]:
    # use case: list -> str
    if len(span_group) != len(labels):
        raise ValueError('labels and span_group are not compatible.')

    output_len = span_group[-1].end
    output_labels = [0] * output_len

    for span, label in zip(span_group, labels):
        for i in range(span.start, span.end):
            output_labels[i] = label

    return output_labels
