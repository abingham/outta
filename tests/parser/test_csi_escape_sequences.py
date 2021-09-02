import pyte.escape
import pytest
from outta.elements import CursorUp, InsertCharacters
from outta.parser import Parser


@pytest.fixture(params=Parser.csi.items(), ids=lambda c: str(c[1]))
def csi_escape_sequence(request):
    return request.param


def test_no_arguments(csi_escape_sequence):
    code, element_type = csi_escape_sequence
    text = f"\u001b[{code}"
    parser = Parser()

    actual = list(parser.feed(text))
    expected = [element_type((0,), {}, text)]
    assert actual == expected


def test_with_arguments(csi_escape_sequence):
    code, element_type = csi_escape_sequence
    count = 5
    text = f"\u001b[{count}{code}"
    parser = Parser()

    actual = list(parser.feed(text))
    expected = [element_type((5,), {}, text)]
    assert actual == expected
