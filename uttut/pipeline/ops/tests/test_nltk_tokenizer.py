import pytest

from ..nltk_tokenizer import NltkTokenizer
from .common_tests_for_pattern_to_token import pattern_to_token_tests


test_cases = {
    True: [
        pytest.param(
            "How's it going today, Mr.Smith?",
            [1, 1, 1, 1, 1, 0, 2, 2, 0, 3, 3, 3, 3, 3, 0, 4, 4, 4, 4, 4, 5, 0,
             6, 6, 6, 6, 6, 6, 6, 6, 7],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?'],
            [1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 7],
            id='punct True',
        ),
    ],
    False: [
        pytest.param(
            "How's it going today, Mr.Smith?",
            [1, 1, 1, 1, 1, 0, 2, 2, 0, 3, 3, 3, 3, 3, 0, 4, 4, 4, 4, 4, 5, 0,
             6, 6, 6, 6, 6, 6, 6, 6, 7],
            ['How', "'s", 'it', 'going', 'today', ',', 'Mr.Smith', '?'],
            [1, 1, 2, 3, 4, 5, 6, 7],
            id='punct False',
        ),
    ],
}


@pytest.fixture
def op():
    return NltkTokenizer(False)


(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases[False])
