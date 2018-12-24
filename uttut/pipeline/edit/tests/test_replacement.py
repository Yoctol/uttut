import pytest

from ..replacement import StrReplacement, LstReplacement


@pytest.mark.parametrize(
    "start,end,new_sequence,annotation,Replacement_type",
    [
        pytest.param(10, 15, '薄餡亂入', None, StrReplacement, id='str-replacement'),
        pytest.param(10, 15, '薄餡亂入', 'ohoh', StrReplacement, id='str-replacement with annotation'),
        pytest.param(10, 15, ['薄餡亂入'], None, LstReplacement, id='list-replacement'),
        pytest.param(10, 15, ['薄餡亂入'], 'ohoh', LstReplacement,
                     id='list-replacement with annotation'),
    ],
)
def test_correctly_init(start, end, new_sequence, annotation, Replacement_type):
    replacement = Replacement_type(
        start=start, end=end, new_sequence=new_sequence, annotation=annotation)
    assert start == replacement.start
    assert end == replacement.end
    assert new_sequence == replacement.new_sequence
    if annotation is None:
        assert replacement.annotation is None
    else:
        assert replacement.annotation == annotation


@pytest.mark.parametrize(
    "start,end,new_sequence,Replacement_type",
    [
        pytest.param(10, 15, ['薄餡亂入'], StrReplacement, id='need str given list'),
        pytest.param(10, 15, '薄餡亂入', LstReplacement, id='need list given str'),
    ],
)
def test_invalid_new_sequence(start, end, new_sequence, Replacement_type):
    with pytest.raises(TypeError):
        Replacement_type(start=start, end=end, new_sequence=new_sequence)


@pytest.mark.parametrize(
    "obj1,obj2",
    [
        pytest.param(StrReplacement(10, 15, '薄餡亂入'), StrReplacement(
            10, 15, '薄餡亂入'), id='no annotation'),
        pytest.param(StrReplacement(10, 15, '薄餡亂入', '1'), StrReplacement(10, 15, '薄餡亂入', '2'),
                     id='different annotation'),
    ],
)
def test_equal(obj1, obj2):
    assert obj1 == obj2


@pytest.mark.parametrize(
    "obj1,obj2",
    [
        pytest.param((10, 15, '薄餡亂入'), StrReplacement(10, 15, '薄餡亂入'),
                     id='str-replacement different type'),
        pytest.param(StrReplacement(10, 15, '薄餡亂入'), StrReplacement(10, 15, '隼興亂入'),
                     id='str-replacement different new_sequence'),
        pytest.param(StrReplacement(10, 15, '薄餡亂入'), StrReplacement(9, 15, '薄餡亂入'),
                     id='str-replacement different start index'),
        pytest.param(StrReplacement(10, 15, '薄餡亂入'), StrReplacement(10, 11, '薄餡亂入'),
                     id='str-replacement different end index'),
        pytest.param((10, 15, ['薄餡亂入']), LstReplacement(10, 15, ['薄餡亂入']),
                     id='lst-replacement different type'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入']), LstReplacement(10, 15, ['隼興亂入']),
                     id='lst-replacement different new_sequence'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入']), LstReplacement(9, 15, ['薄餡亂入']),
                     id='lst-replacement different start index'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入']), LstReplacement(10, 11, ['薄餡亂入']),
                     id='lst-replacement different end index'),
    ],
)
def test_not_equal(obj1, obj2):
    assert obj1 != obj2


@pytest.mark.parametrize(
    "replacement,expected",
    [
        pytest.param(StrReplacement(10, 15, '薄餡亂入'), "(10, 15) => '薄餡亂入'", id='str-replacement'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入']),
                     "(10, 15) => '['薄餡亂入']'", id='lst-replacement'),
    ],
)
def test_str(replacement, expected):
    assert expected == str(replacement)


@pytest.mark.parametrize(
    "replacement,expected",
    [
        pytest.param(StrReplacement(10, 15, '薄餡亂入'),
                     "StrReplacement(10, 15, 薄餡亂入, annotation=None)",
                     id='str-replacement no annotation'),
        pytest.param(StrReplacement(10, 15, '薄餡亂入', 'ohoh'),
                     "StrReplacement(10, 15, 薄餡亂入, annotation=ohoh)",
                     id='str-replacement with annotation'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入']),
                     "LstReplacement(10, 15, ['薄餡亂入'], annotation=None)",
                     id='str-replacement no annotation'),
        pytest.param(LstReplacement(10, 15, ['薄餡亂入'], 'ohoh'),
                     "LstReplacement(10, 15, ['薄餡亂入'], annotation=ohoh)",
                     id='str-replacement with annotation'),
    ],
)
def test_representation(replacement, expected):
    assert expected == repr(replacement)
