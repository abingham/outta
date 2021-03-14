from lark import Lark
from outta.control_code import CursorUp, CursorDown


parser = Lark('''
_stream: (escape_code | text)*

?escape_code: _csi code_param

_csi: "\x1b["
   | "\u001b["
   | "\033["

?code_param: NUMBER "A" -> cursor_up
   | NUMBER "B" -> cursor_down

text: /\w|\s/+ -> regular_text

%import common.WORD
%import common.NUMBER
''', start='_stream')

CODE_MAP = {
    'cursor_up': lambda n: CursorUp(int(n)),
    'cursor_down': lambda n: CursorDown(int(n)),
}


def parse(text):
    accumulated_text = None
    tree = parser.parse(text)
    for child in tree.children:
        if child.data == 'regular_text':
            if accumulated_text is None:
                accumulated_text = ''
            for text_elem in child.children:
                accumulated_text += text_elem.value
        else:
            if accumulated_text is not None:
                yield accumulated_text
                accumulated_text = None
            yield CODE_MAP[child.data](*child.children)
