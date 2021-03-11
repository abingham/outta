"""Internal representation for control codes.

Information gathered from:

* https://notes.burke.libbey.me/ansi-escape-codes/
"""
from collections import OrderedDict


class ControlCode:
    def __init__(self, *args):
        self._args = args

    # TODO: Register subclasses in lookup dict or something.

    @property
    def args(self):
        return self._args

    def __repr__(self):
        return f"{type(self)}(args={self.args})"


class FixedSignatureControlCode(ControlCode):
    def __init__(self, *args):
        if len(args) != len(self.signature):
            raise TypeError(
                f"{type(self)} requires {len(self.signature)} arguments")

        super().__init__(*args)


class CursorUp(FixedSignatureControlCode):
    code = "A"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor up by {self.args[0]}"


class CursorDown(FixedSignatureControlCode):
    code = "B"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor down by {self.args[0]}"


class CursorForward(FixedSignatureControlCode):
    code = "C"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor forward by {self.args[0]}"


class CursorBack(FixedSignatureControlCode):
    code = "D"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor back by {self.args[0]}"


class CursorNextLine(FixedSignatureControlCode):
    code = "E"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor to the beginning of the line {self.args[0]} lines down"


class CursorPreviousLine(FixedSignatureControlCode):
    code = "F"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor to the beginning of the line {self.args[0]} lines up"


class CursorHorizontalAbsolute(FixedSignatureControlCode):
    code = "G"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor to the the column {self.args[0]} within the current row"


class CursorPosition(FixedSignatureControlCode):
    code = "H"
    signature = OrderedDict(n=1, m=1)

    def __str__(self):
        return f"Move cursor to row {self.args[0]}, column {self.args[1]}, counting from the top left corner"


class EraseInDisplay(FixedSignatureControlCode):
    code = "J"
    signature = OrderedDict(n=0)

    def __str__(self):
        # TODO: What are these "specific functions?"
        return (
            "Clear part of the screen. 0, 1, 2, and 3 have various specific functions"
        )


class EraseinLine(FixedSignatureControlCode):
    code = "K"
    signature = OrderedDict(n=0)

    def __str__(self):
        # TODO: What are these "specific functions?"
        return "Clear part of the line. 0, 1, and 2 have various specific functions"


class ScrollUp(FixedSignatureControlCode):
    code = "S"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Scroll window up by {self.args[0]} lines"


class ScrollDown(FixedSignatureControlCode):
    code = "T"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Scroll window down by {self.args[0]} lines"


class SaveCursorPosition(FixedSignatureControlCode):
    code = "s"
    signature = {}

    def __str__(self):
        return "Save current cursor position for use with u"


class RestoreCursorPosition(FixedSignatureControlCode):
    code = "u"
    signature = {}

    def __str__(self):
        return "Set cursor back to position last saved by s"


class CursorHorizontalAbsoluteAlt(FixedSignatureControlCode):
    code = "f"
    signature = OrderedDict(n=1)

    def __str__(self):
        return f"Move cursor to the the column {self.args[0]} within the current row"


class SetGraphicsMode(ControlCode):
    code = "m"
    description = "Set graphics mode"

    def __init__(self, *args):
        if len(args) not in (1, 3, 5):
            raise TypeError(
                f"SGM only accepts 1, 3, or 5 arguments. Received {args}.")

        self._description = self._args_to_description(args)

    def __str__(self):
        return f'Set graphics mode: {self._description}'

    @staticmethod
    def _args_to_description(args):
        match args:
            case(0,):
                return 'Reset: turn off all attributes'

            case(1,):
                return 'Bold / bright'

            case(3,):
                return 'Italic'

            case(4,):
                return 'Underline'

            case(x,) if 30 <= x <= 37:
                color_id = x - 30
                color_name = SetGraphicsMode._basic_color(color_id)
                return f"Set text color to {color_name}"

            case(38, 5, n):
                # TODO: SHould we be guarding against n not in 0-255?
                return f'Set text color to palette color {n}'

            case(38, 2, r, g, b):
                # TODO: Should we be guarding against r,b,g not in 0-255?
                return f'Set text color to R={r} G={g} B={b}'

            case(x,) if 40 <= x <= 47:
                color_id = x - 40
                color_name = SetGraphicsMode._basic_color(color_id)
                return f"Set background color to {color_name}"

            case(48, 5, n):
                # TODO: SHould we be guarding against n not in 0-255?
                return f'Set background color to palette color {n}'

            case(48, 2, r, g, b):
                # TODO: Should we be guarding against r,b,g not in 0-255?
                return f'Set background color to R={r} G={g} B={b}'

            case(x,) if 90 <= x <= 97:
                color_id = x - 90
                color_name = SetGraphicsMode._basic_color(color_id)
                return f"Set text color to {color_name} from the bright color palette"

            case(x,) if 100 <= x <= 107:
                color_id = x - 100
                color_name = SetGraphicsMode._basic_color(color_id)
                return f"Set background color to {color_name} from the bright color palette"

    @staticmethod
    def _basic_color(color_id):
        return {
            0: "black",
            1: "red",
            2: "green",
            3: "yellow",
            4: "blue",
            5: "magenta",
            6: "cyan",
            7: "white",
        }[color_id]

# Another pair of useful escapes is \x1b[?25h and \x1b[?25l. These show and hide the cursor, respectively.

# One other thing that we use frequently is \r, or Carriage Return, which is functionally similar or identical to \x1b[1G


def get_control_code(code, args):
    if code == SetGraphicsMode.code:
        return SetGraphicsMode(*args)

    raise ValueError(f'Unrecognized control code: {code}')
