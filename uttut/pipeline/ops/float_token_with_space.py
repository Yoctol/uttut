import re

from .tokens import FLOAT_TOKEN_WITH_SPACE
from .int_token_with_space import IntTokenWithSpace


class FloatTokenWithSpace(IntTokenWithSpace):

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+\.\d+(?![\.\d])")
    TOKEN = FLOAT_TOKEN_WITH_SPACE

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super(    # type: ignore
            IntTokenWithSpace,
            self,
        )._gen_forward_replacement_group(
            input_str=input_str,
            annotation='float-token-with-space',
        )
