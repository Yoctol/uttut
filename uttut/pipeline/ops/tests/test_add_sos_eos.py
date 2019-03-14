import pytest

from ..add_sos_eos import AddSosEos
from .common_tests import OperatorTestTemplate, ParamTuple


class TestAddSosEos(OperatorTestTemplate):

    params = [
        ParamTuple(
            ['alvin', '喜歡', '吃', '榴槤'],
            [1, 2, 3, 4],
            ['<sos>', 'alvin', '喜歡', '吃', '榴槤', '<eos>'],
            [0, 1, 2, 3, 4, 0],
            'zh',
        ),
    ]

    @pytest.fixture(scope='class')
    def op(self):
        return AddSosEos()

    def test_not_equal(self, op):
        custom_op = AddSosEos(start_token='custom_SOS', end_token='custom_EOS')
        assert custom_op != op
