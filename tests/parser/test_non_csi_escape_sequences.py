import pytest
from outta.parser import Parser


@pytest.fixture(params=Parser.escape.items(), ids=lambda c: str(c[1]))
def non_csi_escape_sequence(request):
    return request.param


def test_non_csi_escape_sequences(non_csi_escape_sequence):
    text, element_type = non_csi_escape_sequence
    text = f"\u001b{text}"

    parser = Parser()

    actual = list(parser.feed(text))
    expected = [element_type((), {}, text)]

    assert actual == expected
