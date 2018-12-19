import pytest

from ..edit import StrEdit, LstEdit, EditGroup


@pytest.mark.filterwarnings("ignore")
def test_correctly_init():
    edit_group = EditGroup()
    assert edit_group._is_done is False
    assert edit_group._edits == set()
    assert len(edit_group) == 0


@pytest.mark.parametrize(
    "dtype,objs",
    [
        pytest.param(StrEdit, [(0, 0, 'a'), (0, 2, 'b')], id='str-edit'),
        pytest.param(StrEdit, [(0, 0, 'a', 'ohoh'), (0, 2, 'b', 'ohoh1')],
                     id='str-edit with annotation'),
        pytest.param(LstEdit, [(0, 0, ['a']), (0, 2, ['b'])], id='list-edit'),
        pytest.param(LstEdit, [(0, 0, ['a'], 'ohoh'), (0, 2, ['b'], 'ohoh1')],
                     id='list-edit with annotation'),
    ],
)
def test_add_all(dtype, objs):
    edit_group = EditGroup.add_all(objs)
    assert edit_group._is_done is True
    assert len(edit_group) == len(objs)
    assert [dtype(*obj) for obj in objs] == edit_group[:]


def test_add_all_empty():
    with pytest.warns(UserWarning, match='EditGroup is empty'):
        EditGroup.add_all([])


@pytest.mark.parametrize(
    "obj,error_type",
    [
        pytest.param([(0,)], ValueError, id='lack of elements'),
        pytest.param([(0, 0, 'a', 'a', 'a')], ValueError, id='has redundant elements'),
        pytest.param([(0, 0, 12.3)], TypeError, id='not supported replacement type'),
        pytest.param([(0, 1, 'a'), (0, 2, ['b'])], TypeError, id='mixed edits'),
    ],
)
def test_add_fails(obj, error_type):
    with pytest.raises(error_type):
        EditGroup.add_all(obj)


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(EditGroup.add_all([]), EditGroup.add_all([]), id='empty'),
        pytest.param(EditGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     EditGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     id='str-edit'),
        pytest.param(EditGroup.add_all([(0, 0, ['a']), (1, 2, ['b'])]),
                     EditGroup.add_all([(0, 0, ['a']), (1, 2, ['b'])]),
                     id='list-edit'),
    ],
)
def test_equal(group1, group2):
    assert group1 == group2


@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(EditGroup.add_all([(0, 0, 'a')]), [(0, 0, 'a')],
                     id='different type'),
        pytest.param(EditGroup.add_all([(0, 0, 'a')]),
                     EditGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     id='different length'),
        pytest.param(EditGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     EditGroup.add_all([(0, 0, 'a'), (1, 3, 'b')]),
                     id='different element'),
        pytest.param(EditGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     EditGroup.add_all([(0, 0, ['a']), (1, 3, ['b'])]),
                     id='different type of edit'),
    ],
)
def test_not_equal(group1, group2):
    assert group1 != group2


@pytest.mark.parametrize(
    "objs,expected_objs",
    [
        pytest.param([(1, 2, 'b'), (0, 1, 'a')], [StrEdit(0, 1, 'a'), StrEdit(1, 2, 'b')]),
    ],
)
def test_need_sorted(objs, expected_objs):
    obj_group = EditGroup.add_all(objs)
    assert expected_objs == obj_group[:]


@pytest.mark.parametrize(
    "objs",
    [
        pytest.param([(1, 10, 'b'), (2, 15, 'a')], id='intersect'),
        pytest.param([(1, 10, 'b'), (2, 8, 'a')], id='include'),
    ],
)
def test_validate_disjoint(objs):
    with pytest.raises(ValueError):
        EditGroup.add_all(objs)


@pytest.mark.parametrize(
    "name,group",
    [
        pytest.param('StrEditGroup', EditGroup.add_all([(0, 0, 'a')]), id='str-edit'),
        pytest.param('LstEditGroup', EditGroup.add_all([(0, 0, ['a'])]), id='list-edit'),
    ],
)
def test_representation(name, group):
    assert name == repr(group)


def test_getitem_fails():
    edit_group = EditGroup()
    edit_group.add(0, 2, 'a')
    with pytest.raises(RuntimeError):
        edit_group[0]
