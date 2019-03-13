import pytest

from ...tests.common_tests import common_test, update_locals
from ..char_tokenizer import CharTokenizer


@pytest.fixture
def op():
    yield CharTokenizer()


test_cases = [
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        ["G", "B", "亂", "入"],
        [1, 1, 2, 2],
        id='zh',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


def test_equal(op):
    assert CharTokenizer() == op
