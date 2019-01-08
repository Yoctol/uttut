from typing import List

import re
from collections import Counter

from .tokens import INT_TOKEN
from .pattern_to_token import PatternRecognizer, PatternRecognizerRealigner


def _forward_transduce_func(labels: List[int], output_size: int) -> List[int]:
    counter = Counter(labels)
    common_label = counter.most_common()[0][0]
    return [common_label] * output_size


class IntToken(PatternRecognizer):
    """
    Recognize integer (ex: 12, 10000) in the input string
    and replace them with INT_TOKEN (_int_)

    E.g.
    >>> from uttut.pipeline.ops.int_token import IntToken
    >>> op = IntToken()
    >>> output_seq, output_labels, realigner = op.transform("10", [1, 1])
    >>> output_seq
    "_int_"
    >>> output_labels
    [1, 1, 1, 1, 1]
    >>> realigner(output_labels)
    [1, 1]

    """

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
    TOKEN = INT_TOKEN

    def __init__(self):
        super().__init__(realigner_class=IntTokenRealigner)

    def _forward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _forward_transduce_func(labels=labels, output_size=output_size)

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(
            input_str=input_str,
            annotation='int-token',
        )


class IntTokenRealigner(PatternRecognizerRealigner):

    def _backward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        nonzero_labels = [l for l in labels if l > 0]
        counter = Counter(nonzero_labels)
        common_label = counter.most_common()[0][0]
        return [common_label] * output_size
