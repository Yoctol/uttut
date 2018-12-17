import pytest

from ..edit import Edit, EditGroup


def test_normal():
    edits = [Edit(0, 0, 'a'), Edit(0, 2, 'b')]
    eg = EditGroup(edits)
    assert edits == eg.edits


def test_need_sorted():
    edits = [Edit(1, 2, 'b'), Edit(0, 1, 'a')]
    eg = EditGroup(edits)
    assert [Edit(0, 1, 'a'), Edit(1, 2, 'b')] == eg.edits


@pytest.mark.parametrize(
    "edits",
    [
        pytest.param([Edit(1, 10, 'b'), Edit(2, 15, 'a')], id='intersect'),
        pytest.param([Edit(1, 10, 'b'), Edit(2, 8, 'a')], id='include'),
    ],
)
def test_validate_disjoint(edits):
    with pytest.raises(ValueError):
        EditGroup(edits)


def test_wrong_type():
    edits = [Edit(1, 10, 'b'), (2, 8, 'a')]
    with pytest.raises(TypeError):
        EditGroup(edits)
