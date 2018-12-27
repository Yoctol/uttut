from typing import List

import re
from collections import Counter

from .pattern_to_token import PatternRecognizer


class IntTokenWithSpace(PatternRecognizer):

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
    TOKEN = " _int_ "

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
