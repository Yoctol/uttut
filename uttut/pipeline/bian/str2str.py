from .edit import EditGroup
from .utils import (
    _transform_sequence,
    _gen_inverse_edit_group,
)


def apply(input_str: str, edit_group: EditGroup) -> str:
    n_edit = len(edit_group)
    output = [''] * (2 * n_edit + 1)
    output_lst = _transform_sequence(
        input_seq=input_str,
        edit_group=edit_group,
        output=output,
    )
    output_str = ''.join(output_lst)
    return output_str


def inverse(input_str: str, edit_group: EditGroup) -> EditGroup:
    inverse_edit_group = _gen_inverse_edit_group(
        input_seq=input_str,
        edit_group=edit_group,
    )
    assert len(inverse_edit_group) == len(edit_group)
    return inverse_edit_group
