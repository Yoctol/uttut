from typing import List

import re
from collections import Counter

from .pattern_to_token import PatternRecognizer


def _get_most_common_label(labels: List[int], output_size: int) -> List[int]:
    counter = Counter(labels)
    common_label = counter.most_common()[0][0]
    return [common_label] * output_size


class MergeWhiteSpaceCharacters(PatternRecognizer):

    REGEX_PATTERN = re.compile(r"\s+")
    TOKEN = " "

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(
            labels=labels,
            output_size=output_size,
        )

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(
            labels=labels,
            output_size=output_size,
        )
