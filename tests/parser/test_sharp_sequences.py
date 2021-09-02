from outta.elements import AlignmentDisplay
from outta.parser import Parser


def test_sharp():
    parser = Parser()

    text = "\u001b#4"
    actual = list(parser.feed(text))
    expected = [AlignmentDisplay((), {}, text)]

    assert actual == expected
