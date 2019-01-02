from typing import List

from .tokenizer import Tokenizer


class CharTokenizer(Tokenizer):

    def _tokenize(self, input_str: str) -> List[str]:
        return list(input_str)

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        return labels
