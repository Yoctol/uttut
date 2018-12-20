from typing import List, Sequence

from .edit import EditGroup


def _transform_sequence(
        input_seq: Sequence,
        edit_group: EditGroup,
        output: Sequence,
    ) -> Sequence:
    '''
    input_seq: list of str or pure str
    '''

    start = 0
    i = 0
    for edit in edit_group:
        output[i] = input_seq[start: edit.start]
        output[i + 1] = edit.replacement
        start = edit.end
        i += 2

    # tail
    output[-1] = input_seq[start:]

    return output


def _gen_inverse_edit_group(
        input_seq: Sequence,
        edit_group: EditGroup,
    ) -> EditGroup:
    '''
    input_seq: list of str or pure str
    '''
    if edit_group.is_empty():
        return EditGroup.add_all([])

    inverse_edit_group = EditGroup()
    n_edit = len(edit_group)

    dists = get_dist_bt_edit_group(edit_group)
    dists.append(0)

    start = edit_group[0].start

    for i in range(n_edit):
        edit = edit_group[i]
        dist = dists[i]
        inverse_edit_group.add(
            start=start,
            end=start + len(edit.replacement),
            replacement=input_seq[edit.start: edit.end],
        )
        start += len(edit.replacement) + dist
    inverse_edit_group.done()
    return inverse_edit_group


def get_dist_bt_edit_group(edit_group: EditGroup) -> List[int]:
    '''Compute the distance between edit_group
    The distance is the length of sequence.
    Eg.
    Given [Edit(0, 1, ''), Edit(4, 7, '')]: [3]  # 4 - 1
    Given [Edit(0, 3, ''), Edit(3, 4, ''), Edit(8, 11, '')]: [0, 4]
    Note that the length of output would be 1 less than that of input edit_group.
    Arg: a list of edit_group
    Return: a list of integers
    '''
    n_edit = len(edit_group)
    dists = [0] * (n_edit - 1)

    for i in range(n_edit - 1):
        dist = edit_group[i + 1].start - edit_group[i].end
        dists[i] = dist

    return dists
