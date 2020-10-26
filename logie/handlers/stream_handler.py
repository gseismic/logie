import sys
from .._level import NOTSET
from .._level import getLevelName
from .base_handler import BaseHandler


class StreamHandler(BaseHandler):

    terminator = '\n'
    def __init__(self, stream=None, level=NOTSET):
        # super(StreamHandler, self).__init__(level)
        super(StreamHandler, self).__init__(level=level)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def flush(self):
        # self.stream.flush()
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, 'flush'):
                self.stream.flush()
        finally:
            self.release()

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

    def set_stream(self, stream):
        if stream is self.stream:
            result = None
        else:
            result = self.stream
            self.acquire()
            try:
                self.flush()
                self.stream = stream
            finally:
                self.release()
        return result

    def __repr__(self):
        level = getLevelName(self.level)
        name = getattr(self.stream, 'name', '')
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)
