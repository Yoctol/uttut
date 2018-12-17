import pytest

from ..edit import Edit
from ..span import Span
from ..group import EditGroup, SpanGroup


GROUP = {'e': EditGroup, 's': SpanGroup}


@pytest.mark.parametrize(
    "dtype,objs",
    [
        pytest.param('e', [Edit(0, 0, 'a'), Edit(0, 2, 'b')], id='edit'),
        pytest.param('s', [Span(0, 0), Span(0, 2)], id='span'),
    ],
)
def test_getitem_all(dtype, objs):
    obj_group = GROUP[dtype](objs)
    assert len(objs) == len(obj_group)


@pytest.mark.parametrize(
    "dtype,objs,expected_objs",
    [
        pytest.param('e', [Edit(1, 2, 'b'), Edit(0, 1, 'a')],
                     [Edit(0, 1, 'a'), Edit(1, 2, 'b')], id='edit'),
        pytest.param('s', [Span(1, 2), Span(0, 1)], [Span(0, 1), Span(1, 2)], id='span'),
    ],
)
def test_need_sorted(dtype, objs, expected_objs):
    obj_group = GROUP[dtype](objs)
    assert expected_objs == obj_group[:]


@pytest.mark.parametrize(
    "dtype,objs",
    [
        pytest.param('e', [Edit(1, 10, 'b'), Edit(2, 15, 'a')], id='edit intersect'),
        pytest.param('e', [Edit(1, 10, 'b'), Edit(2, 8, 'a')], id='edit include'),
        pytest.param('s', [Span(1, 10), Span(2, 15)], id='span intersect'),
        pytest.param('s', [Span(1, 10), Span(2, 8)], id='span include'),
    ],
)
def test_validate_disjoint(dtype, objs):
    with pytest.raises(ValueError):
        GROUP[dtype](objs)


@pytest.mark.parametrize(
    "dtype,objs",
    [
        pytest.param('e', [Edit(1, 10, 'b'), (11, 13, 'a')], id='edit'),
        pytest.param('s', [Span(1, 10), (11, 13)], id='span'),
    ],
)
def test_wrong_type(dtype, objs):
    with pytest.raises(TypeError):
        GROUP[dtype](objs)
