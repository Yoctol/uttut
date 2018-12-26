import re

from .pattern_to_token import PatternRecognizer


class IntTokenWithSpace(PatternRecognizer):

    REGEX_PATTERN = re.compile(r"(?<![\.\d])\d+(?![\.\d])")
    TOKEN = " _int_ "
