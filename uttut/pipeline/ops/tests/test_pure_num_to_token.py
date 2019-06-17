import pytest

from ..pure_num_to_token import PureNumtoToken
from .common_tests import OperatorTestTemplate, ParamTuple
from ..tokens import NUM_TOKEN


class TestPureNumtoTokenDefault(OperatorTestTemplate):

    params = [
        ParamTuple(
            ["100", "W9", "300g", "123"],
            [1, 2, 3, 4],
            [NUM_TOKEN, "W9", "300g", NUM_TOKEN],
            [1, 2, 3, 4],
            id="simple",
        ),
        ParamTuple(
            ["繼良", "有", "100", "億", "元"],
            [1, 2, 3, 4, 5],
            ["繼良", "有", NUM_TOKEN, "億", "元"],
            [1, 2, 3, 4, 5],
            id="zh with pure digits",
        ),
        ParamTuple(
            ["取消", "HSC5", "改", "HSA5"],
            [1, 2, 3, 4],
            ["取消", "HSC5", "改", "HSA5"],
            [1, 2, 3, 4],
            id="zh with not pure digits",
        ),
        ParamTuple(
            ["GB", "亂入"],
            [3, 4],
            ["GB", "亂入"],
            [3, 4],
            id="identity",
        ),
    ]

    @pytest.fixture(scope='class')
    def op(self):
        return PureNumtoToken()


class TestPureNumtoTokenCustom(OperatorTestTemplate):

    params = [
        ParamTuple(
            ["100", "W9", "300g", "123"],
            [1, 2, 3, 4],
            ["123", "W9", "300g", "123"],
            [1, 2, 3, 4],
            id="simple",
        ),
        ParamTuple(
            ["繼良", "有", "100", "億", "元"],
            [1, 2, 3, 4, 5],
            ["繼良", "有", "123", "億", "元"],
            [1, 2, 3, 4, 5],
            id="zh with pure digits",
        ),
        ParamTuple(
            ["取消", "HSC5", "改", "HSA5"],
            [1, 2, 3, 4],
            ["取消", "HSC5", "改", "HSA5"],
            [1, 2, 3, 4],
            id="zh with not pure digits",
        ),
        ParamTuple(
            ["GB", "亂入"],
            [3, 4],
            ["GB", "亂入"],
            [3, 4],
            id="identity",
        ),
    ]

    @pytest.fixture(scope='class')
    def op(self):
        return PureNumtoToken(token='123')
