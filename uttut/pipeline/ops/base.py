from abc import ABC, abstractmethod
from typing import List, Tuple, Any


class Operator(ABC):

    """Base class for Ops

    Sub-classes should implement `transform`

    Attributes:
        input_type: input type of sequence to transform
        output_type: output type of transformed sequence

    """

    def __init__(self, input_type, output_type):
        self._input_type = input_type
        self._output_type = output_type

    def __eq__(self, other):
        self_attrs = (self._input_type, self._output_type)
        other_attrs = (other._input_type, other._output_type)
        return self_attrs == other_attrs

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
        return self._output_type

    @abstractmethod
    def transform(self, input_sequence) -> Tuple[Any, 'LabelAligner']:
        """Transform input_sequence and label

        Transform input_sequence to certain form which meets the output_type
        and updates labels if necessary.

        Args:
            input_sequence (input_type): utterance or tokens

        Returns:
            output_sequence (output_type): the transformed result
            label_aligner (obj): an instance of LabelAligner

        """
        pass


class LabelAligner(ABC):

    def __init__(self, input_sequence, edit, output_length):
        self._input_length = len(input_sequence)
        self._output_length = output_length

        self._input_sequence = input_sequence
        self._forward_edit = edit

    def transform(self, labels: List[int]):
        self._validate_input(labels)
        output_labels = self._transform(labels)
        self._validate_output(output_labels)
        return output_labels

    def inverse_transform(self, labels: List[int]):
        self._validate_output(labels)
        output_labels = self._inverse_transform(labels)
        self._validate_input(output_labels)
        return output_labels

    def _validate_input(self, labels):
        if len(labels) != self._input_length:
            raise ValueError('Invalid input labels')

    def _validate_output(self, labels):
        if len(labels) != self._output_length:
            raise ValueError('Invalid output labels')

    @abstractmethod
    def _transform(self, labels):
        pass

    @abstractmethod
    def _inverse_transform(self, labels):
        pass
