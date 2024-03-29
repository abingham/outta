# A collection of tests for parsing control codes and text in the same stream.
#
# There's nothing terribly systematic here, just some spot-tests to make sure things
# work as expected. Add examples to CORPUS as needed.

import pyte.control as ctrl
import pyte.escape as esc
import pytest
from outta.elements import (CursorDown, CursorPosition, LineFeed, SetIconName,
                            SetMode, SetTitle, SetTitleAndIconName, Text)
from outta.parser import Parser


def _csi(text, *args):
    params = ";".join(map(str, args))
    return f"\u001b[{params}{text}"


CORPUS = (
    (
        ctrl.LF + "hello" + _csi(esc.CUD),
        [
            LineFeed((), {}, ctrl.LF),
            Text((), {}, "hello"),
            CursorDown((0,), {}, _csi(esc.CUD)),
        ],
    ),
    (
        _csi(esc.CUP, 3, 4),
        [
            CursorPosition((3, 4), {}, _csi(esc.CUP, 3, 4)),
        ],
    ),
    (
        # This addresses a problem we found where parsing after a SetTitleAndIconName was not correct.
        "\x1b]0;python\x07\x1b[?25h",
        [
            SetTitleAndIconName((), {"title": "python", "name": "python"}, text="\x1b]0;python\x07"),
            SetMode(parameters=(25,), keywords={"private": True}, text="\x1b[?25h"),
        ]
    ),
    (
        "\x1b[?25h",
        [
            SetMode(parameters=(25,), keywords={"private": True}, text="\x1b[?25h"),
        ]
    ),


)


@pytest.fixture(params=CORPUS)
def example(request):
    return request.param


def test_example(example):
    text, expected = example
    actual = list(Parser().feed(text))
    assert actual == expected
