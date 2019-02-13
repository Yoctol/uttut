cdef class Operator:  # noqa: E999

    cdef _input_type
    cdef _output_type

    cpdef tuple transform(self, input_sequence)
    cpdef void _validate_input(self, input_sequence) except *
    cpdef void _validate_output(self, output_sequence) except *
    cpdef tuple _transform(self, input_sequence)


cdef class LabelAligner:  # noqa: E999

    cdef unsigned int _input_length
    cdef unsigned int _output_length
    cdef readonly _input_sequence
    cdef readonly _forward_edit

    cpdef list transform(self, list labels)
    cpdef list inverse_transform(self, list labels)
    cpdef void _validate_input(self, list labels) except *
    cpdef void _validate_output(self, list labels) except *
    cpdef list _transform(self, list labels)
    cpdef list _inverse_transform(self, list labels)
