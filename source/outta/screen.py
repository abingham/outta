def standard(f):
    def wrapper(self, *args, **kwargs):
        self.emit(f(self, *args, **kwargs))

    return wrapper


class ExplainerScreen:
    def __init__(self, destination):
        self.destination = destination

    def emit(self, message):
        self.destination(message)

    @standard
    def reset(self):
        return "Reset the terminal to its initial state"

    @standard
    def resize(self, lines=None, columns=None):
        # If lines or columns is None, it means to not change that dimension. If neither change, this is a noop.
        return f"Resize screen to {lines} lines and {columns} columns"

    @standard
    def set_margins(self, top=None, bottom=None):
        return f"Set top margin to {top} and bottom margin to {bottom}"

    @standard
    def set_mode(self, *modes, **kwargs):
        return f"Set mode. modes={modes}, kwargs={kwargs}"

    @standard
    def reset_mode(self, *modes, **kwargs):
        return f"Reset mode. modes={modes}, kwargs={kwargs}"

    @standard
    def define_charset(self, code, mode):
        return "Define charset. code={code}, mode={mode}"

    @standard
    def shift_in(self):
        return "Shift in"

    @standard
    def shift_out(self):
        return "Shift out"

    @standard
    def draw(self, data):
        return f"Draw {data}"

    @standard
    def set_title(self, param):
        return f"Set title to {param}"

    @standard
    def set_icon_name(self, param):
        return f"Set icon name to {param}"

    @standard
    def carriage_return(self):
        return "Carriage return"

    @standard
    def index(self):
        return "Index"

    @standard
    def reverse_index(self):
        return "Reverse index"

    @standard
    def linefeed(self):
        """Perform an index and, if :data:`~pyte.modes.LNM` is set, a
        carriage return.
        """
        return "Linefeed"

    @standard
    def tab(self):
        """Move to the next tab space, or the end of the screen if there
        aren't anymore left.
        """
        return "Tab"

    @standard
    def backspace(self):
        """Move cursor to the left one or keep it in its position if
        it's at the beginning of the line already.
        """
        return "Backspace"

    @standard
    def save_cursor(self):
        """Push the current cursor position onto the stack."""
        return "Save cursor"

    @standard
    def restore_cursor(self):
        """Set the current cursor position to whatever cursor is on top
        of the stack.
        """
        return "Restore cursor"

    @standard
    def insert_lines(self, count=1):
        return f"Insert {count} lines"

    @standard
    def delete_lines(self, count=1):
        return f"Delete {count} lines"

    @standard
    def insert_characters(self, count=1):
        return f"Insert {count} blank characters"

    @standard
    def delete_characters(self, count=1):
        return f"Delete {count} characters"

    @standard
    def erase_characters(self, count=1):
        return f"Erase {count} characters"

    @standard
    def erase_in_line(self, how=0, private=False):
        methods = {
            0: "from cursor to end of line",
            1: "from beginning of line to cursor",
            2: "complete line",
        }
        private_str = " [private]" if private else ""
        return f"Erase {methods[how]}{private_str}"

    @standard
    def erase_in_display(self, how=0, private=False, *args, **kwargs):
        methods = {
            0: "from cursor to end of screen",
            1: "from beginning of screen to cursor",
            2: "entire screen",
            3: "entire screen",
        }
        private_str = " [private]" if private else ""
        return f"Erase {methods[how]}{private_str}"

    @standard
    def set_tab_stop(self):
        return f"Set horizontal tab stop at {self.cursor.x}"

    @standard
    def clear_tab_stop(self, how=0):
        methods = {
            0: f"Clear horizontal tab stop at {self.cursor.x}",
            3: "Clear all horizontal tab stops",
        }
        return methods[how]

    @standard
    def ensure_hbounds(self):
        return "Ensure the cursor is within horizontal screen bounds"

    @standard
    def ensure_vbounds(self, use_margins=None):
        return f"Ensure the cursor is within the vertical screen bounds [use margins={use_margins}]"

    @standard
    def cursor_up(self, count=1):
        return f"Move cursor up by {count}"

    @standard
    def cursor_up1(self, count=1):
        return f"Move cursor up {count} lines to column 1"

    @standard
    def cursor_down(self, count=1):
        return f"Move cursor down by {count}"

    @standard
    def cursor_down1(self, count=1):
        return f"Move cursor down {count} lines to column 1"

    @standard
    def cursor_back(self, count=1):
        return f"Move cursor back by {count}"

    @standard
    def cursor_forward(self, count=1):
        return f"Move cursor right by {count}"

    @standard
    def cursor_position(self, line=1, column=1):
        return f"Set cursor position to line {line}, column {column}"

    @standard
    def cursor_to_column(self, column=1):
        return f"Move cursor to column {column} in the current line"

    @standard
    def cursor_to_line(self, line=1):
        return f"Move cursor to line {line} in the current column"

    @standard
    def bell(self, *args):
        return f"Bell"

    @standard
    def alignment_display(self):
        return f"Alignment display: fills screen with upper-case E's for screen focus and alignment."

    @standard
    def select_graphic_rendition(self, *attrs):
        return f"Select graphic rendition: {attrs}"

    @standard
    def report_device_attributes(self, mode=0, **kwargs):
        return f"Report terminal identity. mode={mode}, private={kwargs.get('private', False)}"

    @standard
    def report_device_status(self, mode):
        modes = {
            5: "Report terminal status",
            6: "Report cursor position",
        }
        return modes.get(mode, "Report device status - noop")

    @standard
    def write_process_input(self, data):
        return f"Write process data: {data}"

    @standard
    def debug(self, *args, **kwargs):
        return f"Unrecognized escape sequence. Args={args}, Keyword args={kwargs}"
