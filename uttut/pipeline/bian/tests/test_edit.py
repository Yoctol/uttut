import pytest

from ..edit import StrEdit, LstEdit


@pytest.mark.parametrize(
    "start,end,replacement,annotation,Edit_type",
    [
        pytest.param(10, 15, '薄餡亂入', None, StrEdit, id='str-edit'),
        pytest.param(10, 15, '薄餡亂入', 'ohoh', StrEdit, id='str-edit with annotation'),
        pytest.param(10, 15, ['薄餡亂入'], None, LstEdit, id='list-edit'),
        pytest.param(10, 15, ['薄餡亂入'], 'ohoh', LstEdit, id='list-edit with annotation'),
    ],
)
def test_correctly_init(start, end, replacement, annotation, Edit_type):
    edit = Edit_type(start=start, end=end, replacement=replacement, annotation=annotation)
    assert start == edit.start
    assert end == edit.end
    assert replacement == edit.replacement
    if annotation is None:
        assert edit.annotation is None
    else:
        assert edit.annotation == annotation


@pytest.mark.parametrize(
    "start,end,replacement,Edit_type",
    [
        pytest.param(10, 15, ['薄餡亂入'], StrEdit, id='need str given list'),
        pytest.param(10, 15, '薄餡亂入', LstEdit, id='need list given str'),
    ],
)
def test_invalid_replacement(start, end, replacement, Edit_type):
    with pytest.raises(TypeError):
        Edit_type(start=start, end=end, replacement=replacement)


@pytest.mark.parametrize(
    "obj1,obj2",
    [
        pytest.param(StrEdit(10, 15, '薄餡亂入'), StrEdit(10, 15, '薄餡亂入'), id='no annotation'),
        pytest.param(StrEdit(10, 15, '薄餡亂入', '1'), StrEdit(10, 15, '薄餡亂入', '2'),
                     id='different annotation'),
    ],
)
def test_equal(obj1, obj2):
    assert obj1 == obj2


@pytest.mark.parametrize(
    "obj1,obj2",
    [
        pytest.param((10, 15, '薄餡亂入'), StrEdit(10, 15, '薄餡亂入'),
                     id='str-edit different type'),
        pytest.param(StrEdit(10, 15, '薄餡亂入'), StrEdit(10, 15, '隼興亂入'),
                     id='str-edit different replacement'),
        pytest.param(StrEdit(10, 15, '薄餡亂入'), StrEdit(9, 15, '薄餡亂入'),
                     id='str-edit different start index'),
        pytest.param(StrEdit(10, 15, '薄餡亂入'), StrEdit(10, 11, '薄餡亂入'),
                     id='str-edit different end index'),
        pytest.param((10, 15, ['薄餡亂入']), LstEdit(10, 15, ['薄餡亂入']),
                     id='lst-edit different type'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入']), LstEdit(10, 15, ['隼興亂入']),
                     id='lst-edit different replacement'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入']), LstEdit(9, 15, ['薄餡亂入']),
                     id='lst-edit different start index'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入']), LstEdit(10, 11, ['薄餡亂入']),
                     id='lst-edit different end index'),
    ],
)
def test_not_equal(obj1, obj2):
    assert obj1 != obj2


@pytest.mark.parametrize(
    "edit,expected",
    [
        pytest.param(StrEdit(10, 15, '薄餡亂入'), "(10, 15) => '薄餡亂入'", id='str-edit'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入']), "(10, 15) => '['薄餡亂入']'", id='lst-edit'),

    ],
)
def test_str(edit, expected):
    assert expected == str(edit)


@pytest.mark.parametrize(
    "edit,expected",
    [
        pytest.param(StrEdit(10, 15, '薄餡亂入'), "StrEdit(10, 15, 薄餡亂入, annotation=None)",
                     id='str-edit no annotation'),
        pytest.param(StrEdit(10, 15, '薄餡亂入', 'ohoh'), "StrEdit(10, 15, 薄餡亂入, annotation=ohoh)",
                     id='str-edit with annotation'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入']), "LstEdit(10, 15, ['薄餡亂入'], annotation=None)",
                     id='str-edit no annotation'),
        pytest.param(LstEdit(10, 15, ['薄餡亂入'], 'ohoh'),
                     "LstEdit(10, 15, ['薄餡亂入'], annotation=ohoh)",
                     id='str-edit with annotation'),
    ],
)
def test_representation(edit, expected):
    assert expected == repr(edit)
