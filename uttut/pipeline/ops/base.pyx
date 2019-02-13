cdef class Operator:  # noqa: E999

    """Base class for Operators

    Sub-classes should implement `_transform`

    Attributes:
        input_type: input type of sequence to transform
        output_type: output type of transformed sequence

    """

    def __init__(self, input_type, output_type):
        self._input_type = input_type
        self._output_type = output_type

    def __eq__(self, Operator other):
        self_attrs = (self.input_type, self.output_type)
        other_attrs = (other.input_type, other.output_type)
        return self_attrs == other_attrs

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def input_type(self):
        return self._input_type

    @property
    def output_type(self):
        return self._output_type

    cpdef tuple transform(self, input_sequence):
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

    cpdef void _validate_input(self, input_sequence) except *:
        if not isinstance(input_sequence, self.input_type):
            raise TypeError('Invalid input type')

    cpdef void _validate_output(self, output_sequence) except *:
        if not isinstance(output_sequence, self.output_type):
            raise TypeError('Invalid output type')

    cpdef tuple _transform(self, input_sequence):
        pass


cdef class LabelAligner:

    """Base class for LabelAligners

    Sub-classes should implement `_transform` and `_inverse_transform`

    Attributes:
        input_sequence: utterance or tokens
        output_length (int): the length of transformed sequence
        edit: process of transformation documented by `edit` structure

    """

    def __init__(self, input_sequence, edit, unsigned int output_length):
        self._input_length = len(input_sequence)
        self._output_length = output_length

        self._input_sequence = input_sequence
        self._forward_edit = edit

    cpdef list transform(self, list labels):
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

    cpdef list inverse_transform(self, list labels):
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

    cpdef void _validate_input(self, list labels) except *:
        if len(labels) != self._input_length:
            raise ValueError('Invalid input labels')

    cpdef void _validate_output(self, list labels) except *:
        if len(labels) != self._output_length:
            raise ValueError('Invalid output labels')

    cpdef list _transform(self, list labels):
        pass

    cpdef list _inverse_transform(self, list labels):
        pass
