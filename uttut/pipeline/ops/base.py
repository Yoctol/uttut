from abc import ABC, abstractmethod
from typing import Tuple, List, Union


class Operator(ABC):
    """Base class for Ops
    Sub-classes should implement `transform` and `relabel`.

    Attributes:
        input_type: input type of sequence to transform
        output_type: output type of transformed sequence
    """

    def __init__(self, input_type, output_type):
        self._input_type = input_type
        self._output_type = output_type

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
        return self._output_type

    @abstractmethod
    def transform(
            self,
            input_sequence,
            labels: List[int],
            state: dict = None,
        ) -> Tuple[Union[str, List[str]], List[int], 'Realigner']:

        """Transform input_sequence and label

        Transform input_sequence to certain form which meets the output_type
        and updates labels if necessary.

        Args:
            input_sequence (input_type): utterance or tokens
            labels (ints): has same length of input_sequence
            state (dict): data dependent information (output of fit)

        Returns:
            output (output_type): the transformed result
            labels (ints): has same length as output of transfrom
            realigner (obj): an instance of Realigner
        """
        pass


class Realigner(ABC):

    def __init__(self, edit, length: int):
        self.length = length
        self.edit = edit

    def _validate_input(self, labels: List[int]):
        if len(labels) != self.length:
            raise ValueError('Invalid labels')

    @abstractmethod
    def __call__(self, labels: List[int]) -> List[int]:

        """Realign model labels to original input

        Note that self.edit should not be None when calling this method.

        Args:
            labels (ints): has same length as output of transfrom
            state (dict): data dependent information (output of fit)

        Raise:
            ValueError if length of labels is matched.

        Return:
            labels (ints): has same length as input of transform
        """
        pass
