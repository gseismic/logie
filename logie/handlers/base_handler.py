import sys
import time
import threading
from .._level import _levelToName, _nameToLevel, _checkLevel
from .._level import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
from ..formatter import _default_formatter


class BaseHandler(object):

    def __init__(self, level=NOTSET, formatter=None):
        self.level = _checkLevel(level)
        self.formatter = None
        self.create_lock()

    def set_formatter(self, formatter):
        self.formatter = formatter

    def create_lock(self):
        self.lock = threading.RLock()

    def acquire(self):
        if self.lock:
            self.lock.acquire()

    def release(self):
        if self.lock:
            self.lock.release()

    def flush(self):
        pass

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = _default_formatter
        s = fmt.format(record)
        return fmt.format(record)

    def emit(self, record):
        raise NotImplementedError('emit must be implemented '
                                  'by Handler subclasses')

    def handle(self, record):
        if record:
            self.acquire()
            if record.level >= self.level:
                try:
                    self.emit(record)
                finally:
                    self.release()

    def handle_error(self, record):
        try:
            sys.stderr.write('--- Logging error ---\n')
            sys.stderr.write('Message: %r\n'
                             'Arguments: %s\n' % (record.msg, record.args))
        except Exception:
            sys.stderr.write('Unable to print the message and arguments'
                             ' - possible formatting error.\nUse the'
                             ' traceback above to help find the error.\n'
                            )


if __name__ == '__main__':
    rv = _checkLevel(CRITICAL)
    print(rv)
    rv = _checkLevel('CRITICAL')
    print(rv)
    rv = _checkLevel('info')
    print(rv)
