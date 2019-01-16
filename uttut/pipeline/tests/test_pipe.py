import pytest

from uttut.pipeline.ops import op_factory as default_op_factory
from uttut.elements import Datum, Intent, Entity
from ..pipe import Pipe
from .mock_factory import mock_factory


@pytest.fixture
def fake_pipe():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {'1': 1})
    p_custom.add('Str2Lst', {})
    p_custom.add('Lst2Lst', {})
    return p_custom


@pytest.fixture
def fake_pipe_with_checkpoints():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {'1': 1})
    p_custom.add_checkpoint()
    p_custom.add('Str2Lst', {})
    p_custom.add('Lst2Lst', {})
    p_custom.add_checkpoint()
    return p_custom


@pytest.fixture
def dummy_datum():
    return Datum(
        utterance='123',
        intents=[Intent(1)],
        entities=[
            Entity(label=1, start=0, end=1, value='1'),
            Entity(label=2, start=1, end=2, value='2'),
            Entity(label=3, start=2, end=3, value='3'),
        ],
    )


def test_pipe_init_use_correct_factory():
    p = Pipe()
    assert p.operator_factory == default_op_factory
    p_custom = Pipe(mock_factory)
    assert p_custom.operator_factory == mock_factory


def test_pipe_fails_to_add():
    p = Pipe(mock_factory)
    p.add('Lst2Lst')
    with pytest.raises(TypeError):
        p.add('Str2Str')


def test_transform(fake_pipe, dummy_datum):
    output_seq, intent_labels, entity_labels, realigner, intermediate = fake_pipe.transform(
        dummy_datum)

    assert output_seq == ['1', '2', '3']
    assert intent_labels == [1]
    assert entity_labels == [1, 2, 3]
    assert [] == intermediate.get()
    assert [('123', [1, 2, 3]), ('123', [1, 2, 3]),
            (['1', '2', '3'], [1, 2, 3]), (['1', '2', '3'], [1, 2, 3])] == intermediate[:]

    output = realigner(entity_labels)
    assert output == [1, 2, 3]


def test_transform_with_checkpoints(fake_pipe_with_checkpoints, dummy_datum):
    output = fake_pipe_with_checkpoints.transform(dummy_datum)
    output_seq, intent_labels, entity_labels, realigner, intermediate = output

    assert output_seq == ['1', '2', '3']
    assert intent_labels == [1]
    assert entity_labels == [1, 2, 3]
    assert ('123', [1, 2, 3]) == intermediate.get()
    assert (['1', '2', '3'], [1, 2, 3]) == intermediate.get(1)
    assert [('123', [1, 2, 3]), ('123', [1, 2, 3]),
            (['1', '2', '3'], [1, 2, 3]), (['1', '2', '3'], [1, 2, 3])] == intermediate[:]

    output = realigner(entity_labels)
    assert output == [1, 2, 3]


def test_serialization(fake_pipe):
    serialized_str = fake_pipe.serialize()
    o_pipe = Pipe.deserialize(serialized_str, mock_factory)
    assert fake_pipe == o_pipe


def test_serialization_with_checkpoint(fake_pipe_with_checkpoints):
    serialized_str = fake_pipe_with_checkpoints.serialize()
    o_pipe = Pipe.deserialize(serialized_str, mock_factory)
    assert fake_pipe_with_checkpoints == o_pipe
