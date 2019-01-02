from typing import List, Tuple

import nltk
from nltk.tokenize import WordPunctTokenizer, word_tokenize

from ..edit import str2lst, str2str
from ..edit.label_propagation import (
    propagate_by_replacement_group,
    reduce_by_span_group,
    expand_by_span_group,
)

from .base import Operator


class NltkTokenizer(Operator):

    def __init__(self, punct: bool = False):
        super().__init__(input_type=str, output_type=list)
        self.punct = punct
        if self.punct is True:
            nltk.download('punkt')
            self.tokenizer = WordPunctTokenizer()
        else:
            self.tokenizer = word_tokenize

    def transform(  # type: ignore
            self,
            input_sequence: str,
            labels: List[int],
            state: dict = None,
        ) -> Tuple[List[str], List[int]]:

        tokens = self._tokenize(input_sequence)

        # transform sequence
        forward_replacement_group = str2lst.gen_replacement_group(input_sequence, tokens)
        temp_str = str2str.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = str2str.inverse(input_sequence, forward_replacement_group)

        span_group = str2lst.gen_span_group(temp_str, tokens)

        # labels
        output_labels = propagate_by_replacement_group(labels, forward_replacement_group)
        output_labels = reduce_by_span_group(output_labels, span_group)

        self.update_edit(
            {
                'replacement_group': inverse_replacement_group,
                'span_group': span_group,
            },
        )
        return tokens, output_labels

    def _tokenize(self, input_str: str) -> List[str]:
        output: List[str]
        if self.punct is True:
            output = self.tokenizer.tokenize(input_str)
        else:
            output = self.tokenizer(input_str)
        return output

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        output_labels = expand_by_span_group(labels, self.edit['span_group'])
        output_labels = propagate_by_replacement_group(
            output_labels, self.edit['replacement_group'])
        return output_labels
