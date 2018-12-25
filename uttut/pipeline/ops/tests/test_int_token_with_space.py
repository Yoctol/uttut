import pytest


from ..int_token_with_space import IntTokenWithSpace


test_cases = [
    pytest.param(
        "12 24 3666",
        [1, 1, 0, 2, 2, 0, 3, 3, 3, 3],
        " _int_   _int_   _int_ ",
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 0],
        id='int int int',
    ),
    pytest.param(
        "12.3 1000 3.5",
        [1, 1, 1, 1, 0, 2, 2, 2, 2, 0, 3, 3, 3],
        "12.3  _int_  3.5",
        [1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 3, 3, 3],
        id='float int float',
    ),
    pytest.param(
        "GB亂入",
        [1, 1, 2, 2],
        "GB亂入",
        [1, 1, 2, 2],
        id='identity',
    ),
    pytest.param(
        "GB亂入10次",
        [1, 1, 2, 2, 3, 3, 4],
        "GB亂入 _int_ 次",
        [1, 1, 2, 2, 0, 3, 3, 3, 3, 3, 0, 4],
        id='zh with int',
    ),
]


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_data(input_str, input_labels, output_str, output_labels):
    assert len(input_str) == len(input_labels)
    assert len(output_str) == len(output_labels)


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_transform(input_str, input_labels, output_str, output_labels):
    op = IntTokenWithSpace()
    output = op.transform(input_str, input_labels)
    assert output_str == output[0]
    assert output_labels == output[1]


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_realign_labels(input_str, input_labels, output_str, output_labels):
    op = IntTokenWithSpace()
    op.transform(input_str, input_labels)
    output = op.realign_labels(output_labels)
    assert input_labels == output


@pytest.mark.parametrize("input_str,input_labels,output_str,output_labels", test_cases)
def test_realign_labels_fails(input_str, input_labels, output_str, output_labels):
    op = IntTokenWithSpace()
    with pytest.raises(ValueError):
        op.realign_labels(output_labels)
