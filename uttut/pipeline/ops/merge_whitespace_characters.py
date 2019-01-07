from typing import List

import re
from collections import Counter

from .pattern_to_token import PatternRecognizer, PatternRecognizerRealigner


def _get_most_common_label(labels: List[int], output_size: int) -> List[int]:
    counter = Counter(labels)
    common_label = counter.most_common()[0][0]
    return [common_label] * output_size


class MergeWhiteSpaceCharacters(PatternRecognizer):
    """
    Recognize contiguous whitespace characters in the string
    and replace it with a whitespace character (" ")
    """

    REGEX_PATTERN = re.compile(r"\s+")
    TOKEN = " "

    def __init__(self):
        super().__init__(realigner=MergeWhiteSpaceCharactersRealigner)

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(
            labels=labels,
            output_size=output_size,
        )


class MergeWhiteSpaceCharactersRealigner(PatternRecognizerRealigner):

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(labels=labels, output_size=output_size)
