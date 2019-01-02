import pytest

from ..nltk_tokenizer import NltkTokenizer
from .common_tests_for_pattern_to_token import pattern_to_token_tests
from .test_nltk_tokenizer import test_cases


@pytest.fixture
def op():
    return NltkTokenizer(True)


(
    test_data,
    test_transform,
    test_realign_labels,
    test_realign_labels_fails,
) = pattern_to_token_tests(test_cases[True])
