import pytest


from ..float_token_with_space import FloatTokenWithSpace


test_cases = [
    pytest.param(
        "12.3 2.7 0.7777",
        [1, 1, 1, 1, 0, 2, 2, 2, 0, 3, 3, 3, 3, 3, 3],
        " _float_   _float_   _float_ ",
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0],
        id='float float float',
    ),
    pytest.param(
        "1 2.7 1000",
        [1, 0, 2, 2, 2, 0, 3, 3, 3, 3],
        "1  _float_  1000",
        [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 3, 3, 3, 3],
        id='int float int',
    ),
    pytest.param(
        "12.7.7",
        [1, 2, 3, 4, 5, 6],
        "12.7.7",
        [1, 2, 3, 4, 5, 6],
        id='invalid float',
    ),
    pytest.param(
        "奇利利有12.3億元",
        [1, 1, 1, 2, 3, 3, 3, 3, 3, 3],
        "奇利利有 _float_ 億元",
        [1, 1, 1, 2, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3],
    ),
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        "GB亂入",
        [1, 1, 2, 2],
        id='identity',
    ),
]


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_data(input_str, input_labels, output_str, output_labels):
    assert len(input_str) == len(input_labels)
    assert len(output_str) == len(output_labels)


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_transform(input_str, input_labels, output_str, output_labels):
    op = FloatTokenWithSpace()
    output = op.transform(input_str, input_labels)
    assert output_str == output[0]
    assert output_labels == output[1]


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_realign_labels(input_str, input_labels, output_str, output_labels):
    op = FloatTokenWithSpace()
    op.transform(input_str, input_labels)
    output = op.realign_labels(output_labels)
    assert input_labels == output


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_realign_labels_fails(input_str, input_labels, output_str, output_labels):
    op = FloatTokenWithSpace()
    with pytest.raises(ValueError):
        op.realign_labels(output_labels)
