import pytest

from ..entity import Entity


def test_correctly_init():
    label = 1
    start = 1
    end = 3
    value = '紐約'
    replacements = ['斯堪地那維亞', 'KIX']

    ent = Entity(
        label=label,
        value=value,
        start=start,
        end=end,
        replacements=replacements,
    )
    ent.label == label
    ent.start == start
    ent.value == value
    ent.replacements == set(replacements)


def test_correctly_init_no_replacements():
    label = 1
    start = 1
    end = 3
    value = '紐約'

    ent = Entity(
        label=label,
        value=value,
        start=start,
        end=end,
    )
    ent.label == label
    ent.start == start
    ent.value == value
    ent.replacements == set()


def test_correctly_init_replacements_have_value():
    label = 1
    start = 1
    end = 3
    value = '紐約'
    replacements = ['斯堪地那維亞', 'KIX']

    ent = Entity(
        label=label,
        value=value,
        start=start,
        end=end,
        replacements=replacements + [value],
    )
    ent.label == label
    ent.start == start
    ent.value == value
    ent.replacements == set(replacements)
    ent.n_replacements() == len(set(replacements))


def test_no_replacements():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
    )
    ent.no_replacements() is True


def test_has_replacements():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
        replacements=['台北'],
    )
    ent.no_replacements() is False


def test_from_dict():
    label = 1
    start = 1
    end = 3
    replacements = ['斯堪地那維亞', 'KIX']
    utterance = '去紐約的機票'
    entity = {
        'label': label,
        'start': start,
        'end': end,
        'replacements': replacements,
    }
    ent = Entity.from_dict(entity, utterance)
    isinstance(ent, Entity) is True
    ent.value == utterance[start: end]
    ent.label == label
    ent.start == start
    ent.end == end
    ent.replacements == set(replacements)


def test_from_dict_no_replacements():
    label = 1
    start = 1
    end = 3
    utterance = '去紐約的機票'
    entity = {
        'label': label,
        'start': start,
        'end': end,
    }
    ent = Entity.from_dict(entity, utterance)
    isinstance(ent, Entity) is True
    ent.value == utterance[start: end]
    ent.label == label
    ent.start == start
    ent.end == end


def test_to_dict():
    label = 1
    start = 1
    end = 3
    replacements = ['斯堪地那維亞', 'KIX']
    entity = {
        'label': label,
        'start': start,
        'end': end,
        'replacements': replacements,
    }
    ent = Entity(
        label=label,
        value='紐約',
        start=start,
        end=end,
        replacements=replacements,
    )
    ent_tx = ent.to_dict()
    ent_tx['label'] == entity['label']
    ent_tx['start'] == entity['start']
    ent_tx['end'] == entity['end']
    set(ent_tx['replacements']) == set(entity['replacements'])


def test_to_dict_no_replacement():
    label = 1
    start = 1
    end = 3
    entity = {
        'label': label,
        'start': start,
        'end': end,
    }
    ent = Entity(
        label=label,
        value='紐約',
        start=start,
        end=end,
    )
    ent_tx = ent.to_dict()
    ent_tx['label'] == entity['label']
    ent_tx['start'] == entity['start']
    ent_tx['end'] == entity['end']


def test_equal():
    ent1 = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
        replacements=['台北'],
    )
    ent2 = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
        replacements=['台北'],
    )
    ent1 == ent2


def test_not_equal():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=2,
        replacements=['台北'],
    )
    ent_diff_label = Entity(
        label=2,
        value='紐約',
        start=1,
        end=2,
        replacements=['台北'],
    )
    ent_diff_value = Entity(
        label=1,
        value='新加坡',
        start=1,
        end=2,
        replacements=['台北'],
    )
    ent_diff_start = Entity(
        label=1,
        value='紐約',
        start=0,
        end=2,
        replacements=['台北'],
    )
    ent_diff_end = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
        replacements=['台北'],
    )
    ent_diff_replacements = Entity(
        label=1,
        value='紐約',
        start=1,
        end=2,
        replacements=['台北', 'KIX'],
    )

    ent == ent_diff_label
    ent == ent_diff_value
    ent == ent_diff_start
    ent == ent_diff_end
    ent == ent_diff_replacements


def test_raise_error_if_compare_different_type():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=2,
        replacements=['台北'],
    )
    ent_diff_type = object()
    with pytest.raises(TypeError):
        ent == ent_diff_type
