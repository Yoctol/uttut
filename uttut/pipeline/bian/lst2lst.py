from typing import List

from .edit import EditGroup
from .utils import (
    _transform_sequence,
    _gen_inverse_edit_group,
)


def apply(input_lst: list, edit_group: EditGroup) -> List[str]:
    output: List[list]
    n_edit = len(edit_group)
    output = [[]] * (2 * n_edit + 1)
    output_lst = _transform_sequence(
        input_seq=input_lst,
        edit_group=edit_group,
        output=output,
    )
    return sum(output_lst, [])


def inverse(input_lst: list, edit_group: EditGroup) -> EditGroup:
    inverse_edit_group = _gen_inverse_edit_group(
        input_seq=input_lst,
        edit_group=edit_group,
    )
    assert len(inverse_edit_group) == len(edit_group)
    return inverse_edit_group


# TODO label
