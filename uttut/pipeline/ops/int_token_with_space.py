import re
from typing import List, Tuple
from collections import Counter

from .base import Operator
from ..edit.replacement import ReplacementGroup
from ..edit import str2str
from ..edit.label_propagation import propagate_by_replacement_group


INT_TOKEN_WITH_SPACE_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
INT_TOKEN_WITH_SPACE = " _int_ "


def _gen_forward_replacement_group(input_str: str) -> ReplacementGroup:
    shift = 0
    replacement_group = ReplacementGroup()

    while shift < len(input_str):
        match = INT_TOKEN_WITH_SPACE_PATTERN.search(input_str, shift)
        if match is None:
            break
        replacement_group.add(
            start=match.start(),
            end=match.end(),
            new_value=INT_TOKEN_WITH_SPACE,
        )
        shift = match.end()
    replacement_group.done()
    return replacement_group


def _forward_reduce_func(labels: List[int], output_size: int):
    counter = Counter(labels)
    common_label = counter.most_common()[0][0]
    token_len = len(INT_TOKEN_WITH_SPACE) - 2
    output_label = [0] + [common_label] * token_len + [0]
    return output_label


def _inverse_reduce_func(labels: List[int], output_size: int):
    nonzero_labels = [l for l in labels if l > 0]
    counter = Counter(nonzero_labels)
    common_label = counter.most_common()[0][0]
    return [common_label] * output_size


class IntTokenWithSpace(Operator):

    def __init__(self):
        super().__init__(input_type=str, output_type=str)

    def transform(  # type: ignore
            self,
            input_sequence: str,
            labels: List[int],
            state: dict = None,
        ) -> Tuple[str, List[int]]:

        forward_replacement_group = _gen_forward_replacement_group(input_sequence)
        output_sequence = str2str.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = str2str.inverse(input_sequence, forward_replacement_group)

        self.update_edit(inverse_replacement_group)
        updated_labels = propagate_by_replacement_group(
            labels, forward_replacement_group, _forward_reduce_func)

        return output_sequence, updated_labels

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        return propagate_by_replacement_group(labels, self.edit, _inverse_reduce_func)
