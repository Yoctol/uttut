from typing import List

from .tokenizer import Tokenizer, TokenizerAligner
from .label_transducer import get_most_common_except_not_entity


class CharTokenizer(Tokenizer):

    def __init__(self):
        super().__init__(label_aligner_class=CharTokenizerAligner)

    def _tokenize(self, input_str: str) -> List[str]:
        return list(input_str)


class CharTokenizerAligner(TokenizerAligner):

    def _forward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return get_most_common_except_not_entity(labels, output_size)

    def _backward_transduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return get_most_common_except_not_entity(labels, output_size)
