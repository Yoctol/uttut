from typing import List

import re

from .pattern_to_token import PatternRecognizer


class StripWhiteSpaceCharacters(PatternRecognizer):
    """
    Recognize leading and trailing whitespace characters in the string
    and replace them with an empty string ("")
    """

    REGEX_PATTERN = re.compile(r"\A\s+|\s+\Z")
    TOKEN = ""

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return [0] * output_size

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return [0] * output_size

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(
            input_str=input_str,
            annotation='strip whitespace',
        )
