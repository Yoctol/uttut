import pytest

from uttut.pipeline.ops import op_factory as default_op_factory
from uttut.elements import Datum, Intent, Entity
from ..pipe import Pipe
from .mock_factory import mock_factory


@pytest.fixture
def fake_pipe():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {})
    p_custom.add('Str2Lst', {})
    p_custom.add('Lst2Lst', {})
    return p_custom


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


def test_transform(fake_pipe):
    datum = Datum(
        utterance='123',
        intents=[Intent(1)],
        entities=[
            Entity(label=1, start=0, end=1, value='1'),
            Entity(label=2, start=1, end=2, value='2'),
            Entity(label=3, start=2, end=3, value='3'),
        ],
    )
    output_seq, intent_labels, entity_labels, realigner = fake_pipe.transform(datum)

    assert output_seq == ['1', '2', '3']
    assert intent_labels == [1]
    assert entity_labels == [1, 2, 3]

    output = realigner(entity_labels)
    assert output == [1, 2, 3]


def test_serialization():
    p_custom = Pipe(mock_factory)
    p_custom.add('Str2Str', {'1': 1})

    serialized_str = p_custom.serialize()
    o_pipe = Pipe.deserialize(serialized_str, mock_factory)

    assert p_custom == o_pipe

# def test_add_step_by_op_name_correctly_create_op(mocker):
#     MockOp = Mock()
#     mock_op_name = 'MockOp'
#     mock_factory = _OpFactory()
#     mock_factory.register(mock_op_name,  # noqa: E128
#         MockOp,
#     )
#     p = Pipe(op_factory=mock_factory)

#     p.add_step_by_op_name(mock_op_name)
#     MockOp.assert_called_once_with(**{})


# def test_add_step_by_op_name_correctly_create_op_with_kwargs(mocker):
#     MockOp = Mock()
#     mock_op_name = 'MockOp'
#     mock_factory = _OpFactory()
#     mock_factory.register(mock_op_name,  # noqa: E128
#         MockOp,
#     )
#     expected_kwargs = {'a': 1, '2': 'b'}
#     p = Pipe(op_factory=mock_factory)

#     p.add_step_by_op_name(
#         mock_op_name,
#         op_kwargs=expected_kwargs,
#     )
#     MockOp.assert_called_once_with(**expected_kwargs)


# def test_add_step_by_op_name_raise_if_type_wrong():
#     mock_op_1 = MagicMock(inpur_type=STRING, output_type=STRING)
#     mock_op_2 = MagicMock(inpur_type=STRING_LIST, output_type=STRING)
#     MockOp1 = Mock(return_value=mock_op_1)
#     MockOp2 = Mock(return_value=mock_op_2)

#     mock_factory = _OpFactory()
#     mock_factory.register('MockOp1',  # noqa: E128
#         MockOp1,
#     )
#     mock_factory.register('MockOp2',  # noqa: E128
#         MockOp2,
#     )
#     p = Pipe(op_factory=mock_factory)

#     p.add_step_by_op_name('MockOp1')
#     with pytest.raises(TypeError):
#         p.add_step_by_op_name('MockOp2')


# def test_get_state():
#     mock_op_1 = MagicMock(inpur_type=STRING, output_type=STRING)
#     MockOp1 = Mock(return_value=mock_op_1)

#     mock_factory = _OpFactory()
#     mock_factory.register('MockOp1',  # noqa: E128
#         MockOp1,
#     )
#     p = Pipe(op_factory=mock_factory)
#     p.add_step_by_op_name(
#         'MockOp1',
#         state={
#             '隼興名言': '你的身體不知道你想變強...',
#         },
#     )
#     p.get_state(0) == {
#         '隼興名言': '你的身體不知道你想變強...',
#     }


# def test_add_checkpoint(fake_pipe):
#     fake_pipe.fit('123456')
#     output = fake_pipe.transform('123456')
#     assert output[0] == ['123456_with_state', 'stateless']
#     assert output[2] == ['123456_with_state']


# def test_serialization(fake_pipe, fake_factory):
#     fake_pipe.fit('123456')
#     output_path = Path('.').joinpath('pipe_test/example.json').resolve()
#     output_path.parent.mkdir(exist_ok=True)
#     # save
#     fake_pipe.save_json(output_path)
#     # load
#     restored_pipe = Pipe.restore_from_json(
#         path=output_path,
#         op_factory=fake_factory,
#     )
#     output = restored_pipe.transform('123456')
#     assert output[0] == ['123456_with_state', 'stateless']
#     assert output[2] == ['123456_with_state']

#     with patch('json.dump') as patch_dump:
#         fake_serializable = ['step1']
#         json_dump_kwargs = dict(
#             indent=2,
#             ensure_ascii=False,
#         )
#         fake_pipe._generate_serializable = lambda: fake_serializable
#         fake_pipe.save_json(output_path, json_dump_kwargs)
#         patch_dump.assert_called_once_with(
#             fake_serializable,
#             ANY,  # a filep
#             **json_dump_kwargs,
#         )

#     # teardown
#     shutil.rmtree(str(output_path.parent))
