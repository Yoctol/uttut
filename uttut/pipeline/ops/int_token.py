from typing import List

import re
from collections import Counter

from .tokens import INT_TOKEN
from .pattern_to_token import PatternRecognizer


class IntToken(PatternRecognizer):

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
    TOKEN = INT_TOKEN

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        counter = Counter(labels)
        common_label = counter.most_common()[0][0]
        return [common_label] * output_size

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        nonzero_labels = [l for l in labels if l > 0]
        counter = Counter(nonzero_labels)
        common_label = counter.most_common()[0][0]
        return [common_label] * output_size

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(
            input_str=input_str,
            annotation='int-token',
        )
