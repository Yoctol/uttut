import pytest

from ..edit import Edit
from ..validation import validate_objs


def test_normal():
    edits = [Edit(0, 0, 'a'), Edit(0, 2, 'b')]
    output = validate_objs(edits, Edit)
    assert edits == output


def test_need_sorted():
    edits = [Edit(1, 2, 'b'), Edit(0, 1, 'a')]
    output = validate_objs(edits, Edit)
    assert [Edit(0, 1, 'a'), Edit(1, 2, 'b')] == output


def test_intersection():
    edits = [Edit(1, 10, 'b'), Edit(2, 15, 'a')]
    with pytest.raises(ValueError):
        validate_objs(edits, Edit)


def test_wrapped():
    edits = [Edit(1, 10, 'b'), Edit(2, 8, 'a')]
    with pytest.raises(ValueError):
        validate_objs(edits, Edit)


def test_wrong_type():
    edits = [Edit(1, 10, 'b'), (2, 8, 'a')]
    with pytest.raises(TypeError):
        validate_objs(edits, Edit)
