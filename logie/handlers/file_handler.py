import os
from .._level import NOTSET
from .stream_handler import StreamHandler


class FileHandler(StreamHandler):

    def __init__(self, filename, mode='a', encoding=None, level=NOTSET):
        filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        StreamHandler.__init__(self, self._open(), level=level)

    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        return open(self.baseFilename, self.mode, encoding=self.encoding)

    def close(self):
        self.acquire()
        try:
            if self.stream:
                try:
                    self.flush()
                finally:
                    stream = self.stream
                    self.stream = None
                    if hasattr(stream, 'close'):
                        stream.close()
        finally:
            self.release()

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        StreamHandler.emit(self, record)


class _TimedRotatingFileHandler(StreamHandler):

    def __init__(self, filename, when='D'):
        pass
