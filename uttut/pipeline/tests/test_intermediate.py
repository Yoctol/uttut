from ..intermediate import Intermediate


def _transform(input_lst, index):
    output = input_lst + [index]
    return output


def test_all():
    intm = Intermediate([1, 3])
    input_lst = [0]
    expected_record = []
    for i in range(10):
        input_lst = _transform(input_lst, i)
        intm.add(input_lst)
        expected_record.append(input_lst.copy())
    assert expected_record == intm[:]
    assert expected_record[1] == intm.get()
    assert expected_record[3] == intm.get(1)
