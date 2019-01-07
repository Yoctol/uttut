from typing import List
import re

from .tokens import FLOAT_TOKEN_WITH_SPACE
from .int_token_with_space import IntTokenWithSpaceRealigner, _forward_reduce_func
from .pattern_to_token import PatternRecognizer


class FloatTokenWithSpace(PatternRecognizer):
    """
    Recognize integer (ex: 12.3, 100.77) in the input string
    and replace them with FLOAT_TOKEN_WTIH_SPACE ( _float_ )

    Note that extra spaces are added behind and after the FLOAT_TOKEN.

    E.g.
        I have 10.7 dollars. -> I have  _float_  dollars.
    """

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+\.\d+(?![\.\d])")
    TOKEN = FLOAT_TOKEN_WITH_SPACE

    def __init__(self):
        super().__init__(realigner=IntTokenWithSpaceRealigner)

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(
            input_str=input_str,
            annotation='float-token-with-space',
        )

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _forward_reduce_func(labels=labels, output_size=output_size, token=self.TOKEN)
