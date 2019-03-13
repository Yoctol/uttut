import pytest

from ...tests.common_tests import common_test, update_locals
from ..eng_tokenizer import EngTokenizer


@pytest.fixture
def op():
    return EngTokenizer()


test_cases = [
    pytest.param(
        "How's it going today, Mr.Smith?",
        [1, 1, 1, 1, 1, 0, 2, 2, 0, 3, 3, 3, 3, 3, 0, 4, 4, 4, 4, 4, 5, 0,
         6, 6, 6, 6, 6, 6, 6, 6, 7],
        ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?'],
        [1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7],
        id='the same as nltk with punct',
    ),
    pytest.param(
        "a \t \t \nb",
        [1, 0, 0, 0, 0, 0, 0, 2],
        ["a", "b"],
        [1, 2],
        id='split effect',
    ),
    pytest.param(
        "GB亂入",
        [2, 2, 2, 2],
        ['GB亂入'],
        [2],
        id='eng + zh',
    ),
    pytest.param(
        "",
        [],
        [],
        [],
        id='empty string',
    ),
]


funcs = common_test(test_cases)
update_locals(locals(), funcs)


@pytest.mark.parametrize(
    "input_str,input_labels,expected_output_seq,"
    "expected_output_labels,expected_realigned_labels",
    [
        pytest.param(
            "  a b \n", [10, 0, 1, 3, 2, 0, 7], ['a', 'b'], [1, 2], [0, 0, 1, 0, 2, 0, 0],
            id="whitespaces_at_head_or_tail",
        ),
        pytest.param(
            "  \n", [10, 0, 1], [], [], [0, 0, 0],
            id="all whitespaces",
        ),
        pytest.param(
            "GB亂入", [2, 2, 2, 1], ['GB亂入'], [2], [2, 2, 2, 2],
            id="zh + eng",
        ),
    ],
)
def test_invertible_cases(
        input_str, input_labels,
        expected_output_seq, expected_output_labels,
        expected_realigned_labels,
        op,
    ):
    output_seq, label_aligner = op.transform(input_str)
    assert expected_output_seq == output_seq

    output_labels = label_aligner.transform(input_labels)
    assert expected_output_labels == output_labels

    realigned_labels = label_aligner.inverse_transform(expected_output_labels)
    assert expected_realigned_labels == realigned_labels


def test_equal(op):
    assert EngTokenizer() == op
