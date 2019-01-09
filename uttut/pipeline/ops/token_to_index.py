from typing import List, Tuple, Dict

from .base import Operator, Realigner
from .tokens import UNK_TOKEN

from ..edit import lst2lst
from ..edit.replacement import ReplacementGroup


class Token2Index(Operator):

    """
    Map token (str) to index (int) given token2index dictionary

    Note that token2index should have UNK_TOKEN (<unk>).

    E.g.
    >>> from uttut.pipeline.ops.token_to_index import Token2Index
    >>> op = Token2Index({'I': 1, 'like': 2, 'apples': 3})
    >>> output_seq, output_labels, realigner = op.transform(
        ['I', 'like', 'apples'], [3, 4, 5])
    >>> output_seq
    [1, 2, 3]
    >>> output_labels
    [3, 4, 5]
    >>> realigner(output_labels)
    [3, 4, 5]

    """

    def __init__(
            self,
            token2index: Dict[str, int],
            unk_token: str = UNK_TOKEN,
        ):
        super().__init__(input_type=list, output_type=list)
        self._validate_token2index(token2index, unk_token)
        self.token2index = token2index
        self.unk_token = unk_token

    def _validate_token2index(self, token2index: Dict[str, int], unk_token: str):
        indices = set([index for _, index in token2index.items()])
        if len(token2index) != len(indices):
            raise ValueError("duplicated index")

        start_from_zero = min(indices) == 0
        end_at_size = max(indices) == len(token2index) - 1
        if not (start_from_zero and end_at_size):
            raise ValueError("indices are not continuous.")

        if unk_token not in token2index:
            raise KeyError(f"token2index should have token {unk_token}")

    def transform(
            self,
            input_sequence: List[str],
            labels: List[int],
            state: dict = None,
        ) -> Tuple[List[int], List[int], 'Realigner']:

        forward_replacement_group = self._gen_forward_replacement_group(input_sequence)
        output_sequence = lst2lst.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = lst2lst.inverse(input_sequence, forward_replacement_group)

        realigner = Token2IndexRealigner(
            edit=inverse_replacement_group,
            input_length=len(output_sequence),
            output_length=len(input_sequence),
        )

        return output_sequence, labels, realigner

    def _gen_forward_replacement_group(
            self,
            input_lst: List[str],
            annotation: str = None,
        ) -> ReplacementGroup:

        index: int
        replacement_group = ReplacementGroup()
        for idx, token in enumerate(input_lst):
            if token in self.token2index:
                index = self.token2index[token]
            else:
                index = self.token2index[self.unk_token]
            replacement_group.add(
                start=idx,
                end=idx + 1,
                new_value=[index],
                annotation='token2index',
            )
        replacement_group.done()
        return replacement_group


class Token2IndexRealigner(Realigner):

    def _realign_labels(self, labels: List[int]) -> List[int]:
        return labels
