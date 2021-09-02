import pytest
from outta.elements import ShiftIn, ShiftOut
from outta.parser import Parser


@pytest.fixture(params=Parser.basic.items(), ids=lambda c: str(c[1]))
def basic_control_sequence(request):
    return request.param


NON_UTF8_SEQUENCES = {ShiftOut, ShiftIn}


def test_basic_control_sequences(basic_control_sequence):
    text, element_type = basic_control_sequence
    parser = Parser()
    actual = list(parser.feed(text))
    if element_type in NON_UTF8_SEQUENCES:
        expected = []
    else:
        expected = [element_type((), {}, text)]

    assert actual == expected


def test_basic_control_sequences_without_utf8(basic_control_sequence):
    text, element_type = basic_control_sequence
    parser = Parser()
    parser.use_utf8 = False

    actual = list(parser.feed(text))
    expected = [element_type((), {}, text)]

    assert actual == expected
