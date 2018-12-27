import pytest

from .common_tests_for_pattern_to_token import pattern_to_token_tests
from ..strip_whitespace_characters import StripWhiteSpaceCharacters


@pytest.fixture
def op():
    yield StripWhiteSpaceCharacters()


test_cases = [
    pytest.param(
        " \t\n\r\x0b\x0c ",
        [0, 0, 0, 0, 0, 0, 0],
        "",
        [],
        id='all whitespace characters',
    ),
    pytest.param(
        " abc \n\t ",
        [0, 1, 1, 1, 0, 0, 0, 0],
        "abc",
        [1, 1, 1],
        id='eng with whitespaces',
    ),
    pytest.param(
        "我想要喝多 多 綠",
        [0, 0, 0, 0, 1, 1, 1, 1, 1],
        "我想要喝多 多 綠",
        [0, 0, 0, 0, 1, 1, 1, 1, 1],
        id='inner whitespace',
    ),
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        "GB亂入",
        [1, 1, 2, 2],
        id='identity',
    ),
]

(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)
