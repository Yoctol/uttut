from .replacement cimport ReplacementGroup  # noqa: E999
from .span cimport Span, SpanGroup


cpdef list apply(str input_str, SpanGroup span_group):
    cdef list output_lst
    cdef Span span
    cdef unsigned int i

    _validate_compatibility(input_str, span_group)

    output_lst = [''] * len(span_group)
    for i, span in enumerate(span_group):
        output_lst[i] = input_str[span.start: span.end]

    return output_lst


cdef void _validate_compatibility(str input_str, SpanGroup span_group) except *:
    cdef unsigned int n_spans
    n_spans = len(span_group)
    if n_spans > 0:
        if len(input_str) != span_group[-1].end:
            raise ValueError('Input list and span group is not compatible.')


cpdef SpanGroup gen_span_group(str input_str, list tokens):
    '''Compare string and tokens then generate SpanGroup'''
    cdef unsigned int shift, end
    cdef int start
    cdef SpanGroup span_group
    cdef str token

    if input_str != ''.join(tokens):
        raise ValueError('input_str and tokens are not compatible')

    shift = 0
    span_group = SpanGroup()
    for token in tokens:
        start = input_str.find(token, shift)
        end = start + len(token)
        span_group.add(start, end)
        shift = end
    span_group.done()
    assert len(span_group) == len(tokens)
    return span_group


cpdef ReplacementGroup gen_replacement_group(str input_str, list tokens):
    '''Compare string and tokens then generate ReplacementGroup'''
    cdef unsigned int shift
    cdef int start
    cdef ReplacementGroup replacement_group
    cdef str token

    shift = 0
    replacement_group = ReplacementGroup()
    for token in tokens:
        start = input_str.find(token, shift)
        if start == -1:
            raise ValueError('input_str and tokens are not compatible')
        if input_str[shift: start] != '':
            replacement_group.add(shift, start, '')
        shift = start + len(token)

    if shift != len(input_str):
        replacement_group.add(shift, len(input_str), '')

    replacement_group.done()
    return replacement_group
