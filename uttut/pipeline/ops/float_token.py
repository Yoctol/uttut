from typing import List
import re

from .tokens import FLOAT_TOKEN
from .int_token import IntTokenRealigner, _forward_reduce_func
from .pattern_to_token import PatternRecognizer


class FloatToken(PatternRecognizer):
    """
    Recognize float (ex: 12.3, 1.7) in the input string
    and replace them with FLOAT_TOKEN (_float_)

    E.g.
        I have 10.7 dollars. -> I have _float_ dollars.
    """

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+\.\d+(?![\.\d])")
    TOKEN = FLOAT_TOKEN

    def __init__(self):
        super().__init__(realigner=IntTokenRealigner)

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return _forward_reduce_func(labels=labels, output_size=output_size)

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super()._gen_forward_replacement_group(  # type: ignore
            input_str=input_str,
            annotation='float-token',
        )
