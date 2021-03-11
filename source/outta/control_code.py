"""Internal representation for control codes.

Information gathered from:

* https://notes.burke.libbey.me/ansi-escape-codes/
"""
from collections import OrderedDict


class ControlCode:
    def __init__(self, *args):
        self.args = args

    # TODO: Subclass hook check for required class-level attributes
    # TODO: Register subclasses in lookup dict or something.


class FixedSignatureControlCode(ControlCode):
    def __init__(self, *args):
        if len(args) != len(self.signature):
            raise TypeError(f"{type(self)} requires {len(self.signature)} arguments")

        self.args = args


class CursorUp(FixedSignatureControlCode):
    description = "Move cursor up by n"
    signature = OrderedDict(n=1)
    code = "A"


class CursorDown(FixedSignatureControlCode):
    description = "Move cursor down by n"
    signature = OrderedDict(n=1)
    code = "B"


class CursorForward(FixedSignatureControlCode):
    description = "Move cursor forward by n"
    signature = OrderedDict(n=1)
    code = "C"


class CursorBack(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Move cursor back by n"
    code = "D"


class CursorNextLine(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Move cursor to the beginning of the line n lines down"
    code = "E"


class CursorPreviousLine(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Move cursor to the beginning of the line n lines up"
    code = "F"


class CursorHorizontalAbsolute(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Move cursor to the the column n within the current row"
    code = "G"


class CursorPosition(FixedSignatureControlCode):
    signature = OrderedDict(n=1, m=1)
    description = "Move cursor to row n, column m, counting from the top left corner"
    code = "H"


class EraseInDisplay(FixedSignatureControlCode):
    signature = OrderedDict(n=0)
    description = (
        "Clear part of the screen. 0, 1, 2, and 3 have various specific functions"
    )
    code = "J"


class EraseinLine(FixedSignatureControlCode):
    signature = OrderedDict(n=0)
    description = "Clear part of the line. 0, 1, and 2 have various specific functions"
    code = "K"


class ScrollUp(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Scroll window up by n lines"
    code = "S"


class ScrollDown(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Scroll window down by n lines"
    code = "T"


class SaveCursorPosition(FixedSignatureControlCode):
    signature = {}
    description = "Save current cursor position for use with u"
    code = "s"


class RestoreCursorPosition(FixedSignatureControlCode):
    signature = {}
    description = "Set cursor back to position last saved by s"
    code = "u"


class CursorHorizontalAbsoluteAlt(FixedSignatureControlCode):
    signature = OrderedDict(n=1)
    description = "Move cursor to the the column n within the current row"
    code = "f"


# m 	SGR 	(*) 	Set graphics mode. More below
# 0 	Reset: turn off all attributes
# 1 	Bold (or bright, it’s up to the terminal and the user config to some extent)
# 3 	Italic
# 4 	Underline
# 30–37 	Set text colour from the basic colour palette of 0–7
# 38;5;n 	Set text colour to index n in a 256-colour palette (e.g. \x1b[38;5;34m)
# 38;2;r;g;b 	Set text colour to an RGB value (e.g. \x1b[38;2;255;255;0m)
# 40–47 	Set background colour
# 48;5;n 	Set background colour to index n in a 256-colour palette
# 48;2;r;g;b 	Set background colour to an RGB value
# 90–97 	Set text colour from the bright colour palette of 0–7
# 100–107 	Set background colour from the bright colour palette of 0–7

# The basic colour palette has 8 entries:
#     0: black
#     1: red
#     2: green
#     3: yellow
#     4: blue
#     5: magenta
#     6: cyan
#     7: white

# Another pair of useful escapes is \x1b[?25h and \x1b[?25l. These show and hide the cursor, respectively.

# One other thing that we use frequently is \r, or Carriage Return, which is functionally similar or identical to \x1b[1G