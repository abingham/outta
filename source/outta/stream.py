import pyte
from .screen import ExplainerScreen


class ExplainerStream:
    def __init__(self):
        self._explanations = []
        self._feed_buffer = ""
        self._stream = pyte.Stream(
            screen=ExplainerScreen(destination=self._explanations.append)
        )

    def feed(self, data):
        for char in data:
            plain_text = self._stream._taking_plain_text
            self._feed_buffer += char

            self._stream.feed(char)

            if self._stream._taking_plain_text and not plain_text:
                yield self._feed_buffer, self._explanations
                self._feed_buffer = ""
                self._explanations = []
            elif not self._stream._taking_plain_text and plain_text:
                yield self._feed_buffer, ["Plain text"]
                self._feed_buffer = ""
                self._explanations = []
