import pytest

pytest_parametrize = pytest.mark.parametrize


def update_locals(input_locals, funcs):
    input_locals.update({func.__name__: func for func in funcs})


def common_test(test_cases):

    def test_data(input_sequence, input_labels, output_sequence, output_labels):
        assert len(input_sequence) == len(input_labels)
        assert len(output_sequence) == len(output_labels)

    def test_transform(input_sequence, input_labels, output_sequence, output_labels, op):
        output = op.transform(input_sequence, input_labels)
        assert output_sequence == output[0]
        assert output_labels == output[1]

    def test_realign_labels(input_sequence, input_labels, output_sequence, output_labels, op):
        _, _, realigner = op.transform(input_sequence, input_labels)
        output = realigner(output_labels)
        assert input_labels == output

    argstr = "input_sequence,input_labels,output_sequence,output_labels"
    local_objs = locals()
    funcs = [local_objs[func]
             for func in local_objs if callable(local_objs[func]) and func.startswith('test')]
    return [pytest_parametrize(argstr, test_cases)(f) for f in funcs]
