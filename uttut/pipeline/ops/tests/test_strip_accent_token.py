import pytest

from ..strip_accent_token import StripAccentToken
from .common_tests import common_test, update_locals


@pytest.fixture
def op():
    yield StripAccentToken()


test_cases = [
    pytest.param(
        u"H\u00E9llo",
        [1, 2, 3, 4, 5],
        "Hello",
        [1, 2, 3, 4, 5],
        id='eng',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


def test_equal(op):
    assert op == StripAccentToken()
