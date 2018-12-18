import pytest

from ..edit import StrEdit, LstEdit, EditGroup
from ..span import Span, SpanGroup


@pytest.mark.parametrize(
    "Group,objs",
    [
        pytest.param(EditGroup, [StrEdit(0, 0, 'a'), StrEdit(0, 2, 'b')], id='str-edit'),
        pytest.param(EditGroup, [LstEdit(0, 0, ['a']), LstEdit(0, 2, ['b'])], id='list-edit'),
        pytest.param(SpanGroup, [Span(0, 0), Span(0, 2)], id='span'),
    ],
)
def test_correctly_init(Group, objs):
    obj_group = Group(objs)
    assert objs == obj_group[:]


@pytest.mark.parametrize(
    "Group,objs",
    [
        pytest.param(EditGroup, [StrEdit(0, 0, 'a'), StrEdit(0, 2, 'b'), StrEdit(3, 5, 'c')],
                     id='edit'),
        pytest.param(SpanGroup, [Span(0, 0), Span(0, 2)], id='span'),
    ],
)
def test_len(Group, objs):
    obj_group = Group(objs)
    assert len(objs) == len(obj_group)


@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(EditGroup([StrEdit(0, 0, 'a')]), [StrEdit(0, 0, 'a')],
                     id='edit different type'),
        pytest.param(EditGroup([StrEdit(0, 0, 'a')]),
                     EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 2, 'b')]),
                     id='edit different length'),
        pytest.param(EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 2, 'b')]),
                     EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 3, 'b')]),
                     id='edit different element'),
        pytest.param(EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 2, 'b')]),
                     EditGroup([LstEdit(0, 0, ['a']), LstEdit(1, 3, ['b'])]),
                     id='different type of edit'),
        pytest.param(SpanGroup([Span(0, 1)]), [Span(0, 1)], id='span different type'),
        pytest.param(SpanGroup([Span(0, 1)]),
                     SpanGroup([Span(0, 1), Span(1, 3)]), id='span different length'),
        pytest.param(SpanGroup([Span(0, 1), Span(1, 3)]),
                     SpanGroup([Span(0, 1), Span(1, 4)]), id='span different element'),
    ],
)
def test_not_equal(group1, group2):
    assert group1 != group2


@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 2, 'b')]),
                     EditGroup([StrEdit(0, 0, 'a'), StrEdit(1, 2, 'b')]),
                     id='str-edit'),
        pytest.param(EditGroup([LstEdit(0, 0, ['a']), LstEdit(1, 2, ['b'])]),
                     EditGroup([LstEdit(0, 0, ['a']), LstEdit(1, 2, ['b'])]),
                     id='list-edit'),
        pytest.param(SpanGroup([Span(0, 1), Span(1, 3)]),
                     SpanGroup([Span(0, 1), Span(1, 3)]), id='span'),
    ],
)
def test_equal(group1, group2):
    assert group1 == group2


@pytest.mark.parametrize(
    "Group,objs,expected_objs",
    [
        pytest.param(EditGroup, [StrEdit(1, 2, 'b'), StrEdit(0, 1, 'a')],
                     [StrEdit(0, 1, 'a'), StrEdit(1, 2, 'b')], id='edit'),
        pytest.param(SpanGroup, [Span(1, 2), Span(0, 1)], [Span(0, 1), Span(1, 2)], id='span'),
    ],
)
def test_need_sorted(Group, objs, expected_objs):
    obj_group = Group(objs)
    assert expected_objs == obj_group[:]


@pytest.mark.parametrize(
    "Group,objs",
    [
        pytest.param(EditGroup, [StrEdit(1, 10, 'b'), StrEdit(2, 15, 'a')], id='edit intersect'),
        pytest.param(EditGroup, [StrEdit(1, 10, 'b'), StrEdit(2, 8, 'a')], id='edit include'),
        pytest.param(SpanGroup, [Span(1, 10), Span(2, 15)], id='span intersect'),
        pytest.param(SpanGroup, [Span(1, 10), Span(2, 8)], id='span include'),
    ],
)
def test_validate_disjoint(Group, objs):
    with pytest.raises(ValueError):
        Group(objs)


@pytest.mark.parametrize(
    "Group,objs",
    [
        pytest.param(EditGroup, [StrEdit(1, 10, 'b'), (11, 13, 'a')], id='edit element'),
        pytest.param(SpanGroup, [Span(1, 10), (11, 13)], id='span element'),
    ],
)
def test_wrong_type(Group, objs):
    with pytest.raises(TypeError):
        Group(objs)


@pytest.mark.parametrize(
    "spans",
    [
        pytest.param([Span(0, 1), Span(3, 5)], id='not contiguous'),
        pytest.param([Span(1, 3), Span(3, 5)], id='not start from 0'),
    ],
)
def test_span_group_should_be_contiguous(spans):
    with pytest.raises(ValueError):
        SpanGroup(spans)
