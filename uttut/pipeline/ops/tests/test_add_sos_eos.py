import pytest

from ..add_sos_eos import AddSosEos
from .common_tests import common_test, update_locals


@pytest.fixture
def op():
    yield AddSosEos()


test_cases = [
    pytest.param(
        ['alvin', '喜歡', '吃', '榴槤'],
        [1, 2, 3, 4],
        ['<sos>', 'alvin', '喜歡', '吃', '榴槤', '<eos>'],
        [0, 1, 2, 3, 4, 0],
        id='zh',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


# def test_all(op):
#     output_sequence, label_aligner = op.transform(['alvin', '喜歡', '吃', '榴槤'])
#     assert output_sequence == ['<sos>', 'alvin', '喜歡', '吃', '榴槤', '<eos>']
#     output_labels = label_aligner.align_labels([1, 2, 3, 4])
#     assert output_labels == [0, 1, 2, 3, 4, 0]
#     re_labels = label_aligner.realign_labels([0, 1, 2, 3, 4, 0])
#     assert re_labels == [1, 2, 3, 4]


def test_equal(op):
    assert op == AddSosEos()


def test_not_equal(op):
    custom_op = AddSosEos(start_token='custom_SOS', end_token='custom_EOS')
    assert custom_op != op
