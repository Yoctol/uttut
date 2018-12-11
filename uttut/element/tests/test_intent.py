import pytest

from ..intent import Intent


@pytest.fixture(scope="module")
def intent():
    return {'label': 1, 'obj': Intent(1)}


def test_correctly_init(intent):
    label = intent['label']
    obj = intent['obj']
    label == obj.label


def test_repr(intent):
    obj = intent['obj']
    f"<Intent {obj.label}>" == str(obj)


def test_different_type(intent):
    intent['obj'] != []


def test_different_label(intent):
    intent['obj'] != Intent(intent['label'] + 1)


def test_same_hash(intent):
    obj = intent['obj']
    hash(obj) == hash(Intent(obj.label))


def test_different_hash(intent):
    obj = intent['obj']
    hash(obj) != hash(Intent(obj.label + 1))
