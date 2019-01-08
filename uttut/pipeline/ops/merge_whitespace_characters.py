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

    E.g.
    >>> from uttut.pipeline.ops.merge_whitespace_characters import MergeWhiteSpaceCharacters
    >>> op = MergeWhiteSpaceCharacters()
    >>> output_seq, output_labels, realigner = op.transform("\n\n  \t\t", [1, 1, 1, 1, 1, 1])
    >>> output_seq
    " "
    >>> output_labels
    [0]
    >>> realigner(output_labels)
    [0, 0, 0, 0, 0, 0]

    """

    REGEX_PATTERN = re.compile(r"\s+")
    TOKEN = " "

    def __init__(self):
        super().__init__(realigner_class=MergeWhiteSpaceCharactersRealigner)

    def _forward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(
            labels=labels,
            output_size=output_size,
        )


class MergeWhiteSpaceCharactersRealigner(PatternRecognizerRealigner):

    def _backward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _get_most_common_label(labels=labels, output_size=output_size)
