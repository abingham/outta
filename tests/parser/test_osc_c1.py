from outta.parser import Parser
from outta.elements import SetIconName, SetTitle, SetTitleAndIconName
import pyte.control as ctrl
import pytest


OSC_TERMINATORS = set([ctrl.ST_C0, ctrl.ST_C1, ctrl.BEL])


@pytest.fixture(params=OSC_TERMINATORS)
def osc_terminator(request):
    return request.param


def test_set_icon_name(osc_terminator):
    icon_name = "icon name"
    text = ctrl.OSC_C1 + f"1;{icon_name}" + osc_terminator
    actual = list(Parser().feed(text))
    expected = [SetIconName((), {"name": icon_name}, text)]
    assert actual == expected


def test_set_title(osc_terminator):
    title = "title"
    text = ctrl.OSC_C1 + f"2;{title}" + osc_terminator
    actual = list(Parser().feed(text))
    expected = [SetTitle((), {"title": title}, text)]
    assert actual == expected


def test_set_icon_name_and_title(osc_terminator):
    name = "name"
    text = ctrl.OSC_C1 + f"0;{name}" + osc_terminator
    actual = list(Parser().feed(text))
    expected = [SetTitleAndIconName((), {"title": name, "name": name}, text)]
    assert actual == expected
