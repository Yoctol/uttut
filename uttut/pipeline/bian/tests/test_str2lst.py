import pytest

from ..edit import EditGroup
from ..span import SpanGroup
from uttut.pipeline.bian import str2lst


test_cases = [
    pytest.param(
        '我想要喝200元的珍奶10杯',
        ['我', '想要', '喝', '200元', '的', '珍奶', '10杯'],
        EditGroup.add_all([]),
        SpanGroup.add_all(
            [(0, 1), (1, 3), (3, 4), (4, 8), (8, 9), (9, 11), (11, 14)]),
        EditGroup.add_all([]),
        id='jieba',
    ),
    pytest.param(
        '我想要喝 200 元的珍奶 10 杯',
        ['我', '想要', '喝', ' ', '200', ' ', '元', '的', '珍奶', ' ', '10', ' ', '杯'],
        EditGroup.add_all([]),
        SpanGroup.add_all(
            [(0, 1), (1, 3), (3, 4), (4, 5), (5, 8), (8, 9), (9, 10),
             (10, 11), (11, 13), (13, 14), (14, 16), (16, 17), (17, 18)]),
        EditGroup.add_all([]),
        id='jieba with space',
    ),
    pytest.param(
        "I've been to Japan.",
        ["I", "'", "ve", "been", "to", "Japan", "."],
        EditGroup.add_all([(4, 5, ''), (9, 10, ''), (12, 13, '')]),
        SpanGroup.add_all(
            [(0, 1), (1, 2), (2, 4), (4, 8), (8, 10), (10, 15), (15, 16)]),
        EditGroup.add_all([(4, 4, ' '), (8, 8, ' '), (10, 10, ' ')]),
        id='nltk punct',
    ),
    pytest.param(
        "I've been to Japan.",
        ["I've", "been", "to", "Japan", "."],
        EditGroup.add_all([(4, 5, ''), (9, 10, ''), (12, 13, '')]),
        SpanGroup.add_all(
            [(0, 4), (4, 8), (8, 10), (10, 15), (15, 16)]),
        EditGroup.add_all([(4, 4, ' '), (8, 8, ' '), (10, 10, ' ')]),
        id='nltk',
    ),
]


@pytest.mark.parametrize("input_str,tokens,edit_group,span_group,inverse_edit_group", test_cases)
def test_apply(input_str, tokens, edit_group, span_group, inverse_edit_group):
    output = str2lst.apply(input_str, span_group, edit_group)
    assert tokens == output


@pytest.mark.parametrize("input_str,tokens,edit_group,span_group,inverse_edit_group", test_cases)
def test_inverse(input_str, tokens, edit_group, span_group, inverse_edit_group):
    output = str2lst.inverse(input_str, span_group, edit_group)
    assert (inverse_edit_group, span_group) == output


@pytest.mark.parametrize("input_str,tokens,edit_group,span_group,inverse_edit_group", test_cases)
def test_gen_span_group(input_str, tokens, edit_group, span_group, inverse_edit_group):
    if edit_group.is_empty():
        output = str2lst.gen_span_group(input_str, tokens)
        assert span_group == output
    else:
        with pytest.raises(ValueError, message='input_str and tokens are not compatible.'):
            str2lst.gen_span_group(input_str, tokens)


@pytest.mark.parametrize("input_str,tokens,edit_group,span_group,inverse_edit_group", test_cases)
def test_gen_edit_group(input_str, tokens, edit_group, span_group, inverse_edit_group):
    output = str2lst.gen_edit_group(input_str, tokens)
    assert edit_group == output


@pytest.mark.parametrize(
    'input_str,tokens',
    [
        pytest.param('我想要喝200元的珍奶10杯', ['薄餡', '亂入'], id='zh_all_mismatch'),
        pytest.param('我想要喝珍奶', ['我', '想要', '喝', '多多綠'], id='zh_part_mismatch'),
        pytest.param('我想要喝珍奶', ['珍奶', '我', '想要', '喝'], id='zh_different_order'),
    ],
)
def test_gen_edit_group_fail(input_str, tokens):
    with pytest.raises(ValueError, message='input_str and tokens are not compatible.'):
        str2lst.gen_edit_group(input_str, tokens)
