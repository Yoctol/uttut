import pytest

from ..entity import Entity


def test_no_replacements():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
    )
    assert ent.no_replacements() is True
    assert "<Entity 1: 紐約 at 1 - 3, with replacements: >" == ent.__repr__()


def test_has_replacements():
    ent = Entity(
        label=1,
        value='紐約',
        start=1,
        end=3,
        replacements=['台北'],
    )
    assert ent.no_replacements() is False
    assert "<Entity 1: 紐約 at 1 - 3, with replacements: 台北>" == ent.__repr__()


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
    assert isinstance(ent, Entity) is True
    assert ent.value == '紐約'
    assert ent.label == 1
    assert ent.start == start
    assert ent.end == end
    assert ent.replacements == set(replacements)
    assert ent.__repr__() in [
        "<Entity 1: 紐約 at 1 - 3, with replacements: 斯堪地那維亞, KIX>",
        "<Entity 1: 紐約 at 1 - 3, with replacements: KIX, 斯堪地那維亞>",
    ]


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
    assert isinstance(ent, Entity) is True
    assert ent.value == '紐約'
    assert ent.label == 1
    assert ent.start == start
    assert ent.end == end
    assert ent.replacements == set([])
    assert "<Entity 1: 紐約 at 1 - 3, with replacements: >" == ent.__repr__()


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
    assert ent_tx['label'] == entity['label']
    assert ent_tx['start'] == entity['start']
    assert ent_tx['end'] == entity['end']
    assert set(ent_tx['replacements']) == set(entity['replacements'])


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
    assert ent_tx['label'] == entity['label']
    assert ent_tx['start'] == entity['start']
    assert ent_tx['end'] == entity['end']
    assert 'replacements' not in ent_tx


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
    assert ent1 == ent2


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
    assert ent != ent_diff_label
    assert ent != ent_diff_value
    assert ent != ent_diff_start
    assert ent != ent_diff_end
    assert ent != ent_diff_replacements


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
