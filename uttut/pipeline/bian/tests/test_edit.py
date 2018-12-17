from ..edit import Edit


def test_normal():
    start = 10
    end = 15
    replacement = '薄餡亂入'
    edit = Edit(start, end, replacement)

    assert start == edit.start
    assert end == edit.end
    assert replacement == edit.replacement
    assert edit.annotation is None


def test_all_equal():
    assert Edit(10, 15, '薄餡亂入') == Edit(10, 15, '薄餡亂入')


def test_different_instance():
    assert (10, 15, '薄餡亂入') != Edit(10, 15, '薄餡亂入')


def test_different_annotation():
    assert Edit(10, 15, '薄餡亂入', 'ohoh') == Edit(10, 15, '薄餡亂入', 'ohohoh')


def test_different_replacement():
    assert Edit(10, 15, '薄餡亂入') != Edit(10, 15, '隼興亂入')


def test_different_start():
    assert Edit(10, 15, '薄餡亂入') != Edit(9, 15, '隼興亂入')


def test_different_end():
    assert Edit(10, 15, '薄餡亂入') != Edit(10, 11, '隼興亂入')


def test_str():
    edit = Edit(10, 15, '薄餡亂入')
    assert "(10, 15) => '薄餡亂入'" == str(edit)


def test_repr():
    edit = Edit(10, 15, '薄餡亂入')
    assert"Edit(10, 15, 薄餡亂入, annotation=None)" == repr(edit)
