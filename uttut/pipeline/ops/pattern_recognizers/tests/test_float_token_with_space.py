import pytest

from ...tests.common_tests import common_test, update_locals
from ..float_token_with_space import FloatTokenWithSpace


@pytest.fixture
def op():
    yield FloatTokenWithSpace()


test_cases = [
    pytest.param(
        "12.3 2.7 0.7777",
        [1, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 3, 3, 3],
        " _float_   _float_   _float_ ",
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0],
        id='float float float',
    ),
    pytest.param(
        "1 2.7 1000",
        [1, 0, 2, 2, 2, 0, 3, 3, 3, 3],
        "1  _float_  1000",
        [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 3, 3, 3, 3],
        id='int float int',
    ),
    pytest.param(
        "12.7.7",
        [1, 2, 3, 4, 5, 6],
        "12.7.7",
        [1, 2, 3, 4, 5, 6],
        id='invalid float',
    ),
    pytest.param(
        "9.99",
        [0, 0, 0, 0],
        " _float_ ",
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        id='float with label 0',
    ),
    pytest.param(
        "奇利利有12.3億元",
        [1, 1, 1, 2, 3, 3, 3, 3, 3, 3],
        "奇利利有 _float_ 億元",
        [1, 1, 1, 2, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3],
        id='zh with float',
    ),
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        "GB亂入",
        [1, 1, 2, 2],
        id='identity',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


def test_equal(op):
    assert FloatTokenWithSpace() == op
