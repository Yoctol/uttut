import re

from .pattern_to_token import PatternRecognizer


class FloatTokenWithSpace(PatternRecognizer):
    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+\.\d+(?![\.\d])")
    TOKEN = " _float_ "
