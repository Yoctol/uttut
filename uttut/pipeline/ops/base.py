from abc import ABC, abstractmethod
from inspect import getfullargspec
from typing import Any, Dict, List, Tuple

from .factory import OperatorFactory


op_factory = OperatorFactory()


class Operator(ABC):

    """Base class for Operators

    Sub-classes should implement `_transform`

    Attributes:
        input_type: input type of sequence to transform
        output_type: output type of transformed sequence

    """

    _input_type = None
    _output_type = None

    @classmethod
    def __init_subclass__(cls):
        if cls.is_abstract():
            return

        cls.assert_has_class_attributes(['_input_type', '_output_type'])
        op_factory.register(cls.__name__, cls)

        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            argspec = getfullargspec(original_init)
            self._configs = {
                arg_name: val
                for arg_name, val in zip(
                    argspec.args[1:],  # omit `self`
                    args,
                )
            }
            self._configs.update(kwargs)
            if argspec.defaults:
                self._configs.update({
                    arg_name: default_val
                    for arg_name, default_val in zip(
                        reversed(argspec.args),
                        reversed(argspec.defaults),
                    )
                    if arg_name not in self._configs
                })

        cls.__init__ = __init__

    @classmethod
    def is_abstract(cls):
        if getattr(cls, '__abstractmethods__', None):
            return True
        return False

    @classmethod
    def assert_has_class_attributes(cls, attrs):
        for attr_name in attrs:
            assert getattr(cls, attr_name, None) is not None, \
                f"Concrete class: {cls} should declare `{attr_name}`!"

    @staticmethod
    def deserialize(params: Dict):
        cls_name = params['op_name']
        kwargs = params['op_kwargs']
        return op_factory[cls_name](**kwargs)

    def serialize(self) -> Dict:
        return {
            'op_name': self.__class__.__name__,
            'op_kwargs': self.configs,
        }

    @property
    def configs(self):
        return self._configs

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

    def transform(self, input_sequence) -> Tuple[Any, 'LabelAligner']:
        """Transform input_sequence

        Transform input_sequence to certain form which meets the output_type
        and updates labels if necessary.

        Args:
            input_sequence (input_type): utterance or tokens

        Returns:
            output_sequence (output_type): the transformed result
            label_aligner (obj): an instance of LabelAligner

        """

        self._validate_input(input_sequence)
        output_sequence, label_aligner = self._transform(input_sequence)
        self._validate_output(output_sequence)
        return output_sequence, label_aligner

    def _validate_input(self, input_sequence):
        if not isinstance(input_sequence, self.input_type):
            raise TypeError('Invalid input type')

    def _validate_output(self, output_sequence):
        if not isinstance(output_sequence, self.output_type):
            raise TypeError('Invalid output type')

    @abstractmethod
    def _transform(self, input_sequence) -> Tuple[Any, 'LabelAligner']:
        pass


class LabelAligner(ABC):

    """Base class for LabelAligners

    Sub-classes should implement `_transform` and `_inverse_transform`

    Attributes:
        input_sequence: utterance or tokens
        output_length (int): the length of transformed sequence
        edit: process of transformation documented by `edit` structure

    """

    def __init__(self, input_sequence, edit, output_length: int):
        self._input_length = len(input_sequence)
        self._output_length = output_length

        self._input_sequence = input_sequence
        self._forward_edit = edit

    def transform(self, labels: List[int]) -> List[int]:
        """Update labels according to forward edit

        Args:
            labels (ints): has same length as the input_sequence of Operator.transfrom

        Raise:
            ValueError if length of labels is not matched.

        Return:
            labels (ints): has same length as the output_sequence of Operator.transform

        """
        self._validate_input(labels)
        output_labels = self._transform(labels)
        self._validate_output(output_labels)
        return output_labels

    def inverse_transform(self, labels: List[int]) -> List[int]:
        """Realign model predictions to original input

        Args:
            labels (ints): has same length as the output_sequence of Operator.transfrom

        Raise:
            ValueError if length of labels is not matched.

        Return:
            labels (ints): has same length as the input_sequence of Operator.transform

        """
        self._validate_output(labels)
        output_labels = self._inverse_transform(labels)
        self._validate_input(output_labels)
        return output_labels

    def _validate_input(self, labels: List[int]):
        if len(labels) != self._input_length:
            raise ValueError('Invalid input labels')

    def _validate_output(self, labels: List[int]):
        if len(labels) != self._output_length:
            raise ValueError('Invalid output labels')

    @abstractmethod
    def _transform(self, labels: List[int]) -> List[int]:
        pass

    @abstractmethod
    def _inverse_transform(self, labels: List[int]) -> List[int]:
        pass


class NullLabelAligner(LabelAligner):

    def _transform(self, labels: List[int]):
        return labels

    def _inverse_transform(self, labels):
        return labels
