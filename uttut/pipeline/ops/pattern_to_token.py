from typing import List, Tuple, Pattern

from .base import Operator
from ..edit.replacement import ReplacementGroup
from ..edit import str2str
from ..edit.label_propagation import propagate_by_replacement_group


class PatternRecognizer(Operator):
    '''
    Base class for Operators which recognize text patterns using regular expressions
    and replace them with a predefined token.
    '''

    REGEX_PATTERN: Pattern
    TOKEN: str

    def __init__(self):
        super().__init__(input_type=str, output_type=str)

    def _gen_forward_replacement_group(
            self,
            input_str: str,
            annotation: str = None,
        ) -> ReplacementGroup:

        shift = 0
        replacement_group = ReplacementGroup()

        while shift < len(input_str):
            match = self.REGEX_PATTERN.search(input_str, shift)
            if match is None:
                break
            replacement_group.add(
                start=match.start(),
                end=match.end(),
                new_value=self.TOKEN,
                annotation=annotation,
            )
            shift = match.end()
        replacement_group.done()
        return replacement_group

    def _forward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        raise NotImplementedError

    def _backward_reduce_func(self, labels: List[int], output_size: int) -> List[int]:
        raise NotImplementedError

    def transform(  # type: ignore
            self,
            input_sequence: str,
            labels: List[int],
            state: dict = None,
        ) -> Tuple[str, List[int]]:

        forward_replacement_group = self._gen_forward_replacement_group(input_sequence)
        output_sequence = str2str.apply(input_sequence, forward_replacement_group)
        inverse_replacement_group = str2str.inverse(input_sequence, forward_replacement_group)

        self.update_edit(inverse_replacement_group)
        updated_labels = propagate_by_replacement_group(
            labels, forward_replacement_group, self._forward_reduce_func)

        return output_sequence, updated_labels

    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        if self.edit is None:
            raise ValueError('Please call transform first.')
        return propagate_by_replacement_group(labels, self.edit, self._backward_reduce_func)
