import pytest

from ..validation import validate_start_end


def test_normal():
    output = validate_start_end(1, 3)
    assert (1, 3) == output


def test_wrong_type():
    with pytest.raises(TypeError):
        validate_start_end(12.3, 15)

    with pytest.raises(TypeError):
        validate_start_end(12, 15.7)

    with pytest.raises(TypeError):
        validate_start_end(12.3, 15.7)

    with pytest.raises(TypeError):
        validate_start_end('start', 'end')


def test_negative():
    with pytest.raises(ValueError):
        validate_start_end(-3, 10)

    with pytest.raises(ValueError):
        validate_start_end(0, -7)


def test_end_smaller_than_start():
    with pytest.raises(ValueError):
        validate_start_end(18, 10)
