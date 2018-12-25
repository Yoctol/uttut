from abc import ABC, abstractmethod
from typing import Tuple, List, Union


class Operator(ABC):
    """Base class for Ops
    Sub-classes should implement `transform` and `relabel`.
    Attributes:
        input_type: input type of datum to transform
        output_type: output type of transformed datum
    """

    def __init__(self, input_type, output_type):
        self._input_type = input_type
        self._output_type = output_type
        self.reset_edit()

    def reset_edit(self):
        self.edit = None

    def update_edit(self, edit_group):
        self.edit = edit_group

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
        return self._output_type

    @abstractmethod
    def transform(
            self,
            input_sequence: Union[str, List[str]],
            labels: List[int],
            state: dict = None,
        ) -> Tuple[Union[str, List[str]], List[int]]:
        """Transform input and label and Update self.edit
        Transform input to certain form which meets the output_type
        and updates labels if necessary.
        Args:
            input_sequence (input_type): utterance or tokens
            labels (ints): has same length of input_sequence
            state (dict): data dependent information (output of fit)
        Returns:
            output (output_type): the transformed result
            labels (ints): has same length as output of transfrom
        """
        pass

    @abstractmethod
    def realign_labels(self, labels: List[int], state: dict = None) -> List[int]:
        """Propagate model labels back to original input
        Note that self.edit should not be None.
        Arg:
            labels (ints): has same length as output of transfrom
            state (dict): data dependent information (output of fit)
        Return:
            labels (ints): has same length as input of transform
        """
        pass
