import pytest

from ...tests.common_tests import OperatorTestTemplate, ParamTuple
from ..float_token import FloatToken


class TestFloatToken(OperatorTestTemplate):

    params = [
        ParamTuple(
            "12.3 2.7 0.7777",
            [1, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 3, 3, 3],
            "_float_ _float_ _float_",
            [1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 3, 3, 3, 3, 3, 3, 3],
            id='float float float',
        ),
        ParamTuple(
            "1 2.7 1000",
            [1, 0, 2, 2, 2, 0, 3, 3, 3, 3],
            "1 _float_ 1000",
            [1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 3, 3, 3, 3],
            id='int float int',
        ),
        ParamTuple(
            "12.7.7",
            [1, 2, 3, 4, 5, 6],
            "12.7.7",
            [1, 2, 3, 4, 5, 6],
            id='invalid float',
        ),
        ParamTuple(
            "9.99",
            [0, 0, 0, 0],
            "_float_",
            [0, 0, 0, 0, 0, 0, 0],
            id='float with label 0',
        ),
        ParamTuple(
            "奇利利有12.3億元",
            [1, 1, 1, 2, 3, 3, 3, 3, 3, 3],
            "奇利利有_float_億元",
            [1, 1, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            id='zh with float',
        ),
        ParamTuple(
            "GB亂入",
            [1, 1, 2, 2],
            "GB亂入",
            [1, 1, 2, 2],
            id='identity',
        ),
    ]

    @pytest.fixture(scope='class')
    def op(self):
        return FloatToken()

    def test_equal(self, op):
        assert FloatToken() == op
