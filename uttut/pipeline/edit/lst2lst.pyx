from .replacement cimport ReplacementGroup  # noqa: E999
from .utils cimport (  # noqa: E999, E211
    _transform_sequence,
    _gen_inverse_replacement_group,
)


cpdef list apply(list input_lst, ReplacementGroup replacement_group):
    cdef list output, output_lst, flatten_lst
    cdef unsigned int n_replacement

    n_replacement = len(replacement_group)
    output = [[]] * (2 * n_replacement + 1)
    output_lst = _transform_sequence(
        input_seq=input_lst,
        replacement_group=replacement_group,
        output=output,
    )
    flatten_lst = sum(output_lst, [])
    return flatten_lst


cpdef ReplacementGroup inverse(list input_lst, ReplacementGroup replacement_group):
    cdef ReplacementGroup inverse_replacement_group

    inverse_replacement_group = _gen_inverse_replacement_group(
        input_seq=input_lst,
        replacement_group=replacement_group,
    )
    assert len(inverse_replacement_group) == len(replacement_group)
    return inverse_replacement_group
