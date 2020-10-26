import os
from .._level import NOTSET
from .stream_handler import StreamHandler
from ..formatter import _default_colored_formatter


class ColoredStreamHandler(StreamHandler):

    def __init__(self, stream=None, level=NOTSET):
        StreamHandler.__init__(self, stream=stream, level=level)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = _default_colored_formatter
        # s = fmt.format(record)
        return fmt.format(record)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            # stream.write(self.terminator)
            # self.flush()
            if self.stream and hasattr(self.stream, 'flush'):
                self.stream.flush()
        except Exception:
            import traceback
            traceback.print_exc()
            self.handle_error(record)
