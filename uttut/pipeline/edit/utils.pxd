from .replacement cimport ReplacementGroup  # noqa: E999


cdef object _transform_sequence(
    input_seq,
    ReplacementGroup replacement_group,
    list output,
)

cdef ReplacementGroup _gen_inverse_replacement_group(
    input_seq,
    ReplacementGroup replacement_group,
)

cdef list get_dist_bt_replacement_group(ReplacementGroup replacement_group)
