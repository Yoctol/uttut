import re

from .tokens import FLOAT_TOKEN
from .int_token import IntToken


class FloatToken(IntToken):
    """
    Recognize float (ex: 12.3, 1.7) in the input string
    and replace them with FLOAT_TOKEN (_float_)

    E.g.
        I have 10.7 dollars. -> I have _float_ dollars.
    """

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+\.\d+(?![\.\d])")
    TOKEN = FLOAT_TOKEN

    def _gen_forward_replacement_group(self, input_str: str):  # type: ignore
        return super(IntToken, self)._gen_forward_replacement_group(  # type: ignore
            input_str=input_str,
            annotation='float-token',
        )
