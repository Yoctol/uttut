import pytest

from ..span import Span, SpanGroup


def test_normal():
    spans = [Span(0, 0), Span(0, 2)]
    sg = SpanGroup(spans)
    assert spans == sg.spans


def test_need_sorted():
    spans = [Span(1, 2), Span(0, 1)]
    sg = SpanGroup(spans)
    assert [Span(0, 1), Span(1, 2)] == sg.spans


@pytest.mark.parametrize(
    "spans",
    [
        pytest.param(
            [Span(1, 10), Span(2, 15)],
            id='intersect',
        ),
        pytest.param(
            [Span(1, 10), Span(2, 8)],
            id='include',
        ),
    ],
)
def test_validate_disjoint(spans):
    with pytest.raises(ValueError):
        SpanGroup(spans)


def test_wrong_type():
    spans = [Span(1, 10), (2, 8)]
    with pytest.raises(TypeError):
        SpanGroup(spans)
