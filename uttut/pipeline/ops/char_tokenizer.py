from typing import List, Tuple

from ..edit.span import SpanGroup
from .base import Operator


class CharTokenizer(Operator):

    def __init__(self):
        super().__init__(input_type=str, output_type=list)

    def transform(  # type: ignore
            self,
            input_sequence: str,
            labels: List[int],
            state: dict = None,
        ) -> Tuple[List[str], List[int]]:

        output_sequence = list(input_sequence)

        span_group = self._gen_span_group(input_sequence)
        self.update_edit(span_group)

        return output_sequence, labels

    def _gen_span_group(self, input_sequence):
        seqlen = len(input_sequence)
        span_group = SpanGroup.add_all(
            [(ind, ind + 1) for ind in range(seqlen)],
        )
        return span_group

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        return labels
