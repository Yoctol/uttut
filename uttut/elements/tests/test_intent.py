from ..intent import Intent


def test_init():
    intent_label = 1
    intent = Intent(intent_label)
    assert intent.label == intent_label


def test_representation():
    intent_label = 1
    intent = Intent(intent_label)
    assert f"<Intent {self.intent_label}>" == intent.__repr__()
