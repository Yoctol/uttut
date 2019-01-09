import pytest

from ..eng_tokenizer import EngTokenizer
from .common_tests_for_pattern_to_token import pattern_to_token_tests


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


@pytest.fixture
def op():
    return EngTokenizer()


(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases)


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
    output_seq, output_labels, realigner = op.transform(input_str, input_labels)
    assert expected_output_seq == output_seq
    assert expected_output_labels == output_labels

    realigned_labels = realigner(output_labels)
    assert expected_realigned_labels == realigned_labels
