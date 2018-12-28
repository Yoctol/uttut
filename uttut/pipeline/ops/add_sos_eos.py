from typing import List, Tuple

from .base import Operator
from .tokens import START_TOKEN, END_TOKEN

from ..edit import lst2lst
from ..edit.replacement import ReplacementGroup
from ..edit.label_propagation import propagate_by_replacement_group


class AddSosEos(Operator):
    """Add start token (<sos>) and end token (<eos>) to a sequence.

    E.g.
        ['I', 'have', '10.7', 'dollars', '.']
        -> ['<sos>', 'I', 'have', '10.7', 'dollars', '.', '<eos>']
    """

    def __init__(
            self,
            start_token: str = START_TOKEN,
            end_token: str = END_TOKEN,
        ):
        super().__init__(input_type=list, output_type=list)
        self.start_token = start_token
        self.end_token = end_token

    def transform(  # type: ignore
            self,
            input_sequence: List[str],
            labels: List[int],
            state: dict = None,
        ) -> Tuple[List[str], List[int]]:

        forward_replacement_group = self._gen_forward_replacement_group(input_sequence)
        output_sequence = lst2lst.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = lst2lst.inverse(input_sequence, forward_replacement_group)

        self.update_edit(inverse_replacement_group)
        updated_labels = propagate_by_replacement_group(
            labels, forward_replacement_group, self._forward_reduce_func)

        return output_sequence, updated_labels

    def _gen_forward_replacement_group(
            self,
            input_lst: List[str],
            annotation: str = None,
        ) -> ReplacementGroup:

        seqlen = len(input_lst)
        replacement_group = ReplacementGroup.add_all(
            [
                (0, 0, [self.start_token]),  # insert start token
                (seqlen, seqlen, [self.end_token]),  # insert end token
            ],
        )
        return replacement_group

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return [0] * output_size

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        return propagate_by_replacement_group(labels, self.edit, self._backward_reduce_func)

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        return [0] * output_size
