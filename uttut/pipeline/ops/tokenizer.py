from typing import List, Tuple

from ..edit import str2str, str2lst
from ..edit.label_propagation import (
    propagate_by_replacement_group,
    reduce_by_span_group,
    expand_by_span_group,
)

from .base import Operator, LabelAligner


class Tokenizer(Operator):
    """
    Base class for Operators which tokenize text.
    """

    def __init__(self, label_aligner_class):
        super().__init__(input_type=str, output_type=list)
        self._label_aligner_class = label_aligner_class

    def __eq__(self, other):
        same_label_aligner_class = self._label_aligner_class == other._label_aligner_class
        return same_label_aligner_class and super().__eq__(other)

    def _transform(self, input_sequence: str) -> Tuple[List[str], 'LabelAligner']:

        tokens = self._tokenize(input_sequence)

        # transform sequence
        forward_replacement_group = str2lst.gen_replacement_group(input_sequence, tokens)
        temp_str = str2str.apply(input_sequence, forward_replacement_group)
        span_group = str2lst.gen_span_group(temp_str, tokens)

        label_aligner = self._label_aligner_class(
            input_sequence=input_sequence,
            edit={
                'replacement_group': forward_replacement_group,
                'span_group': span_group,
            },
            output_length=len(tokens),
        )

        return tokens, label_aligner

    def _tokenize(self, input_str: str) -> List[str]:
        raise NotImplementedError


class TokenizerAligner(LabelAligner):

    def _transform(self, labels: List[int]):
        output_labels = propagate_by_replacement_group(
            labels=labels,
            replacement_group=self._forward_edit['replacement_group'],
            transduce_func=self._forward_transduce_func,
        )
        output_labels = reduce_by_span_group(output_labels, self._forward_edit['span_group'])
        return output_labels

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        raise NotImplementedError

    def _inverse_transform(self, labels):
        inverse_replacement_group = str2str.inverse(
            self._input_sequence, self._forward_edit['replacement_group'])
        output_labels = expand_by_span_group(
            labels=labels,
            span_group=self._forward_edit['span_group'],
        )
        output_labels = propagate_by_replacement_group(
            labels=output_labels,
            replacement_group=inverse_replacement_group,
            transduce_func=self._backward_transduce_func,
        )
        return output_labels

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        raise NotImplementedError
