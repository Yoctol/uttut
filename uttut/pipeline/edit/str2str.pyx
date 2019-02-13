from .replacement cimport ReplacementGroup  # noqa: E999
from .utils cimport (  # noqa: E211
    _transform_sequence,
    _gen_inverse_replacement_group,
)


cpdef str apply(str input_str, ReplacementGroup replacement_group):
    cdef unsigned int n_replacement
    cdef list output, output_lst
    cdef str output_str

    n_replacement = len(replacement_group)
    output = [''] * (2 * n_replacement + 1)
    output_lst = _transform_sequence(
        input_seq=input_str,
        replacement_group=replacement_group,
        output=output,
    )
    output_str = ''.join(output_lst)
    return output_str


cpdef ReplacementGroup inverse(str input_str, ReplacementGroup replacement_group):
    cdef ReplacementGroup inverse_replacement_group

    inverse_replacement_group = _gen_inverse_replacement_group(
        input_seq=input_str,
        replacement_group=replacement_group,
    )
    assert len(inverse_replacement_group) == len(replacement_group)
    return inverse_replacement_group
