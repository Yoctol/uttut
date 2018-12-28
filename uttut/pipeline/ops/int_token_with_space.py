from typing import List

import re
from collections import Counter

from .tokens import INT_TOKEN_WITH_SPACE
from .pattern_to_token import PatternRecognizer


class IntTokenWithSpace(PatternRecognizer):
    """
    Recognize integer (ex: 12, 10000) in the input string
    and replace them with INT_TOKEN_WTIH_SPACE ( _int_ )

    E.g.
        I have 10 apples. -> I have  _int_  apples.
    """

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
    TOKEN = INT_TOKEN_WITH_SPACE

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        counter = Counter(labels)
        common_label = counter.most_common()[0][0]
        token_len = len(self.TOKEN) - 2
        output_label = [0] + [common_label] * token_len + [0]
        return output_label

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        nonzero_labels = [l for l in labels if l > 0]
        counter = Counter(nonzero_labels)
        common_label = counter.most_common()[0][0]
        return [common_label] * output_size

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(
            input_str=input_str,
            annotation='int-token-with-space',
        )
