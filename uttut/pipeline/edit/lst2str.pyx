from .span cimport Span, SpanGroup  # noqa: E999


cpdef str apply(list input_lst, SpanGroup span_group):
    cdef str output_str

    _validate_compatibility(input_lst, span_group)

    # apply span group (list -> str)
    output_str = ''.join(input_lst)
    return output_str


cdef void _validate_compatibility(list input_lst, SpanGroup span_group) except *:
    cdef unsigned int i
    cdef Span span

    if len(input_lst) != len(span_group):
        raise ValueError('Input list and span group have different length.')
    for i, (token, span) in enumerate(zip(input_lst, span_group)):
        if len(token) != span.end - span.start:
            raise ValueError(f"{i}-th element is not compatible.")
