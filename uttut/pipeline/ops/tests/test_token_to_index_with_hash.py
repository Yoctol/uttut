import pytest

from ..token_to_index_with_hash import Token2IndexwithHash
from .common_tests import common_test, update_locals
from ..utils.consistent_hash import consistent_hash


@pytest.fixture
def token2index():
    return {'oh': 0, '薄餡': 1, '要': 2, '帶': 3, '妹': 4}


@pytest.fixture
def op(token2index):
    yield Token2IndexwithHash(token2index)


def hash_unknown(key):
    return consistent_hash(key, 5)


test_cases = [
    pytest.param(
        ['薄餡', '要', '帶', '櫻花', '妹', '回來'],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, hash_unknown('櫻花'), 4, hash_unknown('回來')],
        [1, 2, 3, 4, 5, 6],
        id='zh',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


@pytest.mark.parametrize(
    'error,token2index',
    [
        pytest.param(
            ValueError, {'薄餡': 1, '要': 1, '帶': 3, '妹': 4},
            id='duplicated indices',
        ),
        pytest.param(
            ValueError, {'薄餡': 0, '要': 2, '帶': 3, '妹': 4},
            id='indices not continuous',
        ),
    ],
)
def test_invalid_token2index(error, token2index):
    with pytest.raises(error):
        Token2IndexwithHash(token2index=token2index)


def test_equal(op, token2index):
    assert op == Token2IndexwithHash(token2index)


def test_not_equal(op):
    op1 = Token2IndexwithHash(token2index={'薄餡': 0, '要': 1, '帶': 2, '妹': 3})
    assert op != op1
