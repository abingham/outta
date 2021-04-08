from typing import Iterable, Mapping, Any


class Element:
    def __init__(
        self, parameters: Iterable[Any], keywords: Mapping[str, Any], text: str
    ):
        self._parameters = tuple(parameters)
        self._keywords = dict(keywords)
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def keywords(self):
        return self._keywords

    @property
    def parameters(self):
        return self._parameters

    def __getitem__(self, index):
        if isinstance(index, str):
            return self.keywords[str]
        return self.parameters[index]

    def __repr__(self):
        return f"{type(self).__name__}(parameters={self.parameters}, keywords={self.keywords}, text={repr(self.text)})"


class AlignmentDisplay(Element):
    pass


class Backspace(Element):
    pass


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


class ShiftIn(Element):
    pass


class Shiftout(Element):
    pass


class Tab(Element):
    pass


class Text(Element):
    def __str__(self):
        return self.text