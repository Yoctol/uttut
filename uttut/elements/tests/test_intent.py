from ..intent import Intent


def test_init():
    intent_label = 1
    intent = Intent(intent_label)
    assert intent.label == intent_label


def test_representation():
    intent_label = 1
    intent = Intent(intent_label)
    assert f"<Intent {intent_label}>" == intent.__repr__()


def test_equal():
    intent_1 = Intent(1)
    intent_2 = Intent(1)
    assert intent_1 == intent_2
