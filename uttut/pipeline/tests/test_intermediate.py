import pytest
from ..intermediate import Intermediate


def _transform(input_lst, index):
    output = input_lst + [index]
    return output


def test_all():
    intm = Intermediate([1, 3], ['name_of_checkpoint1', 'name_of_checkpoint2'])
    input_lst = [0]
    expected_record = []
    for i in range(10):
        input_lst = _transform(input_lst, i)
        intm.add(input_lst)
        expected_record.append(input_lst.copy())
    assert expected_record == intm[:]
    assert expected_record[1] == intm.get_by_checkpoint_index(0) == intm['name_of_checkpoint1']
    assert expected_record[3] == intm.get_by_checkpoint_index(1) == intm['name_of_checkpoint2']

    with pytest.raises(KeyError) as excinfo:
        intm['not-exist-checkpoint']
    assert 'not-exist-checkpoint' in str(excinfo.value)
