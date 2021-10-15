# -*- coding: utf-8 -*-
"""Parse text streams for control sequences, escape codes, etc.

This is based heavily on the work in the pyte project: https://github.com/selectel/pyte

These are the copyrights for the pyte work:

    :copyright: (c) 2011-2012 by Selectel.
    :copyright: (c) 2012-2017 by pyte authors and contributors,
                    see AUTHORS for details.
    :license: LGPL, see LICENSE for more details.

Also, this is beautiful: https://terminalguide.namepad.de/seq/
"""

from __future__ import absolute_import, unicode_literals

import re
from collections import defaultdict
from typing import Iterable

from pyte import control as ctrl
from pyte import escape as esc

from . import elements


class Parser:
    """Parses a stream of text and produces a sequence of ``Element``s.

    This sequence is an representation of the control sequences, escape codes,
    and regular text it finds. It can be used, for example, to drive a terminal
    implementation, for debugging or understanding control sequences, or
    any number of other purposes.

    Args:
        strict: check if a given screen implements all required events.
    """

    #: Control sequences, which don't require any arguments.
    basic = {
        ctrl.BEL: elements.Bell,
        ctrl.BS: elements.Backspace,
        ctrl.HT: elements.Tab,
        ctrl.LF: elements.LineFeed,
        ctrl.VT: elements.LineFeed,
        ctrl.FF: elements.LineFeed,
        ctrl.CR: elements.CarriageReturn,
        ctrl.SO: elements.ShiftOut,
        ctrl.SI: elements.ShiftIn,
    }

    #: non-CSI escape sequences.
    escape = {
        esc.RIS: elements.Reset,
        esc.IND: elements.Index,
        esc.NEL: elements.LineFeed,
        esc.RI: elements.ReverseIndex,
        esc.HTS: elements.SetTabStop,
        esc.DECSC: elements.SaveCursor,
        esc.DECRC: elements.RestoreCursor,
    }

    #: "sharp" escape sequences -- ``ESC # <N>``.
    sharp = {
        esc.DECALN: elements.AlignmentDisplay,
    }

    #: CSI escape sequences -- ``CSI P1;P2;...;Pn <fn>``.
    csi = {
        esc.ICH: elements.InsertCharacters,
        esc.CUU: elements.CursorUp,
        esc.CUD: elements.CursorDown,
        esc.CUF: elements.CursorForward,
        esc.CUB: elements.CursorBack,
        esc.CNL: elements.CursorDown1,
        esc.CPL: elements.CursorUp1,
        esc.CHA: elements.CursorToColumn,
        esc.CUP: elements.CursorPosition,
        esc.ED: elements.EraseInDisplay,
        esc.EL: elements.EraseInLine,
        esc.IL: elements.InsertLines,
        esc.DL: elements.DeleteLines,
        esc.DCH: elements.DeleteCharacters,
        esc.ECH: elements.EraseCharacters,
        esc.HPR: elements.CursorForward,
        esc.DA: elements.ReportDeviceAttributes,
        esc.VPA: elements.CursorToLine,
        esc.VPR: elements.CursorDown,
        esc.HVP: elements.CursorPosition,
        esc.TBC: elements.ClearTabStop,
        esc.SM: elements.SetMode,
        esc.RM: elements.ResetMode,
        esc.SGR: elements.SelectGraphicRendition,
        esc.DSR: elements.ReportDeviceStatus,
        esc.DECSTBM: elements.SetMargins,
        esc.HPA: elements.CursorToColumn,
    }

    #: "select charset" -- ``ESC % <code>``
    percent = {
        '8': elements.EnableUTF8Mode,
        'G': elements.EnableUTF8Mode,
        '@': elements.DisableUTF8Mode,
    }

    #: A regular expression pattern matching everything what can be
    #: considered plain text.
    _special = set([ctrl.ESC, ctrl.CSI_C1, ctrl.NUL, ctrl.DEL, ctrl.OSC_C1])
    _special.update(basic)
    _text_pattern = re.compile("[^" + "".join(map(re.escape, _special)) + "]+")
    del _special

    def __init__(self, strict=True):
        self.strict = strict
        self.use_utf8 = True

        self._parser = None
        self._initialize_parser()

    @property
    def use_utf8(self) -> bool:
        """Whether to operate in "utf8" mode.

        See http://www.cl.cam.ac.uk/~mgk25/unicode.html#term for more details
        on what this means and how utf8 relates to terminal emulators.
        """
        return self._use_utf8

    @use_utf8.setter
    def use_utf8(self, flag: bool):
        self._use_utf8 = flag

    def feed(self, data: str) -> Iterable[elements.Element]:
        """Consume some data and advances the state as necessary.

        Args:
            data: a blob of data to feed from.

        Returns:
            An iterable of Element's.
        """
        send = self._send_to_parser
        match_text = self._text_pattern.match
        taking_plain_text = self._taking_plain_text

        length = len(data)
        offset = 0

        while offset < length:
            if taking_plain_text:
                match = match_text(data, offset)
                if match:
                    start, offset = match.span()
                    yield elements.Text((), {}, data[start:offset])
                else:
                    taking_plain_text = False
                    self._buffer = ""
            else:
                self._buffer += data[offset]
                result = send(data[offset])
                if result is not None:
                    yield result[0](result[1], result[2], self._buffer)
                    taking_plain_text = True
                offset += 1

        self._taking_plain_text = taking_plain_text

    def _send_to_parser(self, data):
        try:
            return self._parser.send(data)
        except Exception:
            # Reset the parser state to make sure it is usable even
            # after receiving an exception. See PR #101 for details.
            self._initialize_parser()
            raise

    def _initialize_parser(self):
        self._buffer = ""
        self._taking_plain_text = True
        self._parser = self._parser_fsm()
        next(self._parser)

    def _parser_fsm(self):
        """An FSM implemented as a coroutine.

        This generator is not the most beautiful, but it is as performant
        as possible. When a process generates a lot of output, then this
        will be the bottleneck, because it processes just one character
        at a time.

        Don't change anything without profiling first.
        """
        basic = self.basic

        ESC, CSI_C1 = ctrl.ESC, ctrl.CSI_C1
        OSC_C1 = ctrl.OSC_C1
        SP_OR_GT = ctrl.SP + ">"
        NUL_OR_DEL = ctrl.NUL + ctrl.DEL
        CAN_OR_SUB = ctrl.CAN + ctrl.SUB
        ALLOWED_IN_CSI = "".join([ctrl.BEL, ctrl.BS, ctrl.HT, ctrl.LF, ctrl.VT, ctrl.FF, ctrl.CR])
        OSC_TERMINATORS = set([ctrl.ST_C0, ctrl.ST_C1, ctrl.BEL])

        def create_dispatcher(mapping):
            return defaultdict(lambda: elements.Debug, mapping)

        basic_dispatch = create_dispatcher(basic)
        sharp_dispatch = create_dispatcher(self.sharp)
        escape_dispatch = create_dispatcher(self.escape)
        csi_dispatch = create_dispatcher(self.csi)
        percent_dispatch = create_dispatcher(self.percent)

        sequence_buffer = ""
        result = None
        while True:
            char = yield result
            sequence_buffer += char

            result = None

            if char == ESC:
                # Most non-VT52 commands start with a left-bracket after the
                # escape and then a stream of parameters and a command; with
                # a single notable exception -- :data:`escape.DECOM` sequence,
                # which starts with a sharp.
                #
                # .. versionchanged:: 0.4.10
                #
                #    For compatibility with Linux terminal stream also
                #    recognizes ``ESC % C`` sequences for selecting control
                #    character set. However, in the current version these
                #    are noop.
                char = yield
                if char == "[":
                    char = CSI_C1  # Go to CSI.
                elif char == "]":
                    char = OSC_C1  # Go to OSC.
                else:
                    if char == "#":
                        result = sharp_dispatch[(yield)], (), {}
                    elif char == "%":
                        result = percent_dispatch[(yield)], (), {}
                    elif char in "()":
                        code = yield
                        if self.use_utf8:
                            continue

                        # See http://www.cl.cam.ac.uk/~mgk25/unicode.html#term
                        # for the why on the UTF-8 restriction.
                        result = "define_charset", (), {"code": code, "mode": char}
                    else:
                        result = escape_dispatch[char], (), {}
                    continue  # Don't go to CSI.

            if char in basic:
                # Ignore shifts in UTF-8 mode. See
                # http://www.cl.cam.ac.uk/~mgk25/unicode.html#term for
                # the why on UTF-8 restriction.
                if (char == ctrl.SI or char == ctrl.SO) and self.use_utf8:
                    continue

                result = basic_dispatch[char], (), {}
            elif char == CSI_C1:
                # All parameters are unsigned, positive decimal integers, with
                # the most significant digit sent first. Any parameter greater
                # than 9999 is set to 9999. If you do not specify a value, a 0
                # value is assumed.
                #
                # .. seealso::
                #
                #    `VT102 User Guide <http://vt100.net/docs/vt102-ug/>`_
                #        For details on the formatting of escape arguments.
                #
                #    `VT220 Programmer Ref. <http://vt100.net/docs/vt220-rm/>`_
                #        For details on the characters valid for use as
                #        arguments.
                params = []
                current = ""
                private = False
                while True:
                    char = yield
                    if char == "?":
                        private = True
                    elif char in ALLOWED_IN_CSI:
                        result = basic_dispatch[char], (), {}
                    elif char in SP_OR_GT:
                        pass  # Secondary DA is not supported atm.
                    elif char in CAN_OR_SUB:
                        # If CAN or SUB is received during a sequence, the
                        # current sequence is aborted; terminal displays
                        # the substitute character, followed by characters
                        # in the sequence received after CAN or SUB.
                        result = elements.Text, (char,), {}
                        break
                    elif char.isdigit():
                        current += char
                    elif char == "$":
                        # XTerm-specific ESC]...$[a-z] sequences are not
                        # currently supported.
                        yield
                        break
                    else:
                        params.append(min(int(current or 0), 9999))

                        if char == ";":
                            current = ""
                        else:
                            if private:
                                result = csi_dispatch[char], params, {"private": True}
                            else:
                                result = csi_dispatch[char], params, {}
                            break  # CSI is finished.
            elif char == OSC_C1:
                code = yield
                if code == "R":
                    continue  # Reset palette. Not implemented.
                elif code == "P":
                    continue  # Set palette. Not implemented.

                param = ""
                while True:
                    char = yield
                    if char == ESC:
                        char += yield
                    if char in OSC_TERMINATORS:
                        break
                    else:
                        param += char

                param = param[1:]  # Drop the ;.
                if code == "0":
                    result = elements.SetTitleAndIconName, (), {"name": param, "title": param}
                elif code == "1":
                    result = elements.SetIconName, (), {"name": param}
                elif code == "2":
                    result = elements.SetTitle, (), {"title": param}
            elif char not in NUL_OR_DEL:
                result = elements.Text, char, {}
