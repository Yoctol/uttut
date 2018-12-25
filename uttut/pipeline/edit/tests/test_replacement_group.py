import pytest

from ..replacement import StrReplacement, LstReplacement, ReplacementGroup


@pytest.mark.filterwarnings("ignore")
def test_correctly_init():
    replacement_group = ReplacementGroup()
    assert replacement_group._is_done is False
    assert replacement_group.is_empty() is True
    assert len(replacement_group) == 0


@pytest.mark.parametrize(
    "dtype,objs",
    [
        pytest.param(StrReplacement, [(0, 0, 'a'), (0, 2, 'b')], id='str-replacement'),
        pytest.param(StrReplacement, [(0, 0, 'a', 'ohoh'), (0, 2, 'b', 'ohoh1')],
                     id='str-replacement with annotation'),
        pytest.param(LstReplacement, [(0, 0, ['a']), (0, 2, ['b'])], id='list-replacement'),
        pytest.param(LstReplacement, [(0, 0, ['a'], 'ohoh'), (0, 2, ['b'], 'ohoh1')],
                     id='list-replacement with annotation'),
    ],
)
def test_add_all(dtype, objs):
    replacement_group = ReplacementGroup.add_all(objs)
    assert replacement_group._is_done is True
    assert len(replacement_group) == len(objs)
    assert [dtype(*obj) for obj in objs] == replacement_group[:]


def test_add_all_empty():
    replacement_group = ReplacementGroup.add_all([])
    assert replacement_group.is_empty() is True


def test_not_done_warning():
    replacement_group = ReplacementGroup()
    with pytest.warns(UserWarning, match='ReplacementGroup needs validation, please call `done`.'):
        len(replacement_group)


def test_not_done_error():
    replacement_group = ReplacementGroup()
    replacement_group.add(1, 3, 'abc')
    with pytest.raises(RuntimeError, message='Please call `done` first.'):
        replacement_group[0]


@pytest.mark.parametrize(
    "obj,error_type",
    [
        pytest.param([(0,)], ValueError, id='lack of elements'),
        pytest.param([(0, 0, 'a', 'a', 'a')], ValueError, id='has redundant elements'),
        pytest.param([(0, 0, 12.3)], TypeError, id='not supported replacement type'),
        pytest.param([(0, 1, 'a'), (0, 2, ['b'])], TypeError, id='mixed replacements'),
    ],
)
def test_add_fails(obj, error_type):
    with pytest.raises(error_type):
        ReplacementGroup.add_all(obj)


@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(ReplacementGroup.add_all([]), ReplacementGroup.add_all([]), id='empty'),
        pytest.param(ReplacementGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     ReplacementGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     id='str-replacement'),
        pytest.param(ReplacementGroup.add_all([(0, 0, ['a']), (1, 2, ['b'])]),
                     ReplacementGroup.add_all([(0, 0, ['a']), (1, 2, ['b'])]),
                     id='list-replacement'),
    ],
)
def test_equal(group1, group2):
    assert group1 == group2


@pytest.mark.parametrize(
    "group1,group2",
    [
        pytest.param(ReplacementGroup.add_all([(0, 0, 'a')]), [(0, 0, 'a')],
                     id='different type'),
        pytest.param(ReplacementGroup.add_all([(0, 0, 'a')]),
                     ReplacementGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     id='different length'),
        pytest.param(ReplacementGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     ReplacementGroup.add_all([(0, 0, 'a'), (1, 3, 'b')]),
                     id='different element'),
        pytest.param(ReplacementGroup.add_all([(0, 0, 'a'), (1, 2, 'b')]),
                     ReplacementGroup.add_all([(0, 0, ['a']), (1, 3, ['b'])]),
                     id='different type of replacement'),
    ],
)
def test_not_equal(group1, group2):
    assert group1 != group2


@pytest.mark.parametrize(
    "objs,expected_objs",
    [
        pytest.param([(1, 2, 'b'), (0, 1, 'a')], [
                     StrReplacement(0, 1, 'a'), StrReplacement(1, 2, 'b')]),
    ],
)
def test_need_sorted(objs, expected_objs):
    obj_group = ReplacementGroup.add_all(objs)
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
        ReplacementGroup.add_all(objs)


@pytest.mark.parametrize(
    "name,group",
    [
        pytest.param('StrReplacementGroup', ReplacementGroup.add_all(
            [(0, 0, 'a')]), id='str-replacement'),
        pytest.param('LstReplacementGroup', ReplacementGroup.add_all(
            [(0, 0, ['a'])]), id='list-replacement'),
        pytest.param('EmptyReplacementGroup', ReplacementGroup.add_all([]), id='empty'),
    ],
)
def test_representation(name, group):
    assert name == repr(group)
