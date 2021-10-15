"""Intermediate representation of the control codes outta recognizes.

One of outta's primary jobs is parsing text streams into sequences of objects representing the control codes it sees,
i.e. the intermediate representation. This module provides the classes that comprise that IR.

For each control sequence outta recognizes, this has a class which contains its parsed contents.
"""

from typing import Iterable, Mapping, Any


class Element:
    """Base class for all control code intermediate representations.

    Args:
        parameters: Iterable of positional arguments to the Element.
        keywords: Dict-like of keyword arguments to the Element.
        text: The text parsed to create the Element (i.e. the control sequence).
    """

    def __init__(self, parameters: Iterable[Any], keywords: Mapping[str, Any], text: str):
        self._parameters = tuple(parameters)
        self._keywords = dict(keywords)
        self._text = text

    @property
    def text(self):
        "The text that was parsed to produce the Element."
        return self._text

    @property
    def keywords(self):
        "Keyword arguments provided to the Element."
        return self._keywords

    @property
    def parameters(self):
        "Positional arguments provided to the Element."
        return self._parameters

    def __getitem__(self, index):
        """Get a positional or keyword argument by index or name.

        Args:
            index: If a string, the name of the keyword argument to retrieve. If an integer, the index
                of the positional argument to retrieve.

        Returns:
            The specified keyword or positional argument.

        Raises:
            IndexError: The integer index is out of bounds.
            KeyError: The string key does not exist in the keywords.
        """
        if isinstance(index, str):
            return self.keywords[str]
        return self.parameters[index]

    def __repr__(self):
        return f"{type(self).__name__}(parameters={self.parameters}, keywords={self.keywords}, text={repr(self.text)})"

    def __eq__(self, rhs):
        return (self._parameters == rhs._parameters) and (self._keywords == rhs._keywords) and (self._text == rhs._text)


# TODO: Add any appropriate methods to the classes below. See CursorDown as an example.
# In particular, __str__ should produce a natural language description of what the
# Element does. This is used for producing human-readable descriptions of what a sequence
# text does.


class AlignmentDisplay(Element):
    pass


class Backspace(Element):
    def __str__(self):
        return "Move cursor back one column"


class Bell(Element):
    pass


class CarriageReturn(Element):
    pass


class ClearTabStop(Element):
    pass


class CursorBack(Element):
    pass


class CursorDown(Element):
    @property
    def count(self):
        return self[0]

    def __str__(self):
        return f"Move cursor down {self.count} rows"


class CursorDown1(Element):
    pass


class CursorForward(Element):
    pass


class CursorPosition(Element):
    pass


class CursorToColumn(Element):
    pass


class CursorToLine(Element):
    pass


class CursorUp(Element):
    @property
    def count(self):
        return self[0]

    def __str__(self):
        return f"Move cursor up {self.count} rows"


class CursorUp1(Element):
    pass


class Debug(Element):
    def __str__(self):
        return f"Invalid control character: {repr(self.text)}"


class DefineCharset(Element):
    pass


class DeleteCharacters(Element):
    pass


class DeleteLines(Element):
    pass


class Draw(Element):
    pass


class EraseCharacters(Element):
    pass


class EraseInDisplay(Element):
    pass


class EraseInLine(Element):
    @property
    def how(self):
        methods = {
            0: "from cursor to end of line",
            1: "from beginning of line to cursor",
            2: "complete line",
        }
        return methods[self[0]]

    @property
    def private(self):
        return self["private"]


class Index(Element):
    pass


class InsertCharacters(Element):
    pass


class InsertLines(Element):
    pass


class LineFeed(Element):
    pass


class ReportDeviceAttributes(Element):
    pass


class ReportDeviceStatus(Element):
    pass


class Reset(Element):
    pass


class ResetMode(Element):
    pass


class RestoreCursor(Element):
    pass


class ReverseIndex(Element):
    pass


class SaveCursor(Element):
    pass


class SelectGraphicRendition(Element):
    pass


class SetIconName(Element):
    @property
    def name(self):
        return self["name"]


class SetMargins(Element):
    pass


class SetMode(Element):
    pass


class SetTabStop(Element):
    pass


class SetTitle(Element):
    @property
    def title(self):
        return self["title"]


class SetTitleAndIconName(SetIconName, SetTitle):
    pass


class ShiftIn(Element):
    pass


class ShiftOut(Element):
    pass


class Tab(Element):
    pass


class EnableUTF8Mode(Element):
    pass


class DisableUTF8Mode(Element):
    pass


class Text(Element):
    def __str__(self):
        return self.text
