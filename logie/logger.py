import os
import sys
import time
import inspect
import threading
from .log_record import LogRecord
from ._level import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL, _checkLevel


def get_caller_info_slow(): 
    # slow
    callerframerecord = inspect.stack()[1]    # 0 represents this line
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    return info.filename, info.function, info.lineno


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else: 
    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


# faster than get_caller_info_slow
def get_caller_info():
    """Return the frame object for the caller's stack frame."""
    f = currentframe()
    return (f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


class Logger(object):

    _lock = threading.Lock()
    def __init__(self, name='root', level=NOTSET, 
                 raise_if_exception=True, 
                 log_thread=True,
                 log_multiprocessing=True,
                 log_process=True,
                 use_utc=False):
        self.name = name
        self.set_level(level)
        self.handlers = []
        self.disabled = False
        self.raise_if_exception = raise_if_exception
        self.log_thread = log_thread
        self.log_multiprocessing = log_multiprocessing
        self.log_process = log_process
        self.use_utc = use_utc

    def update_config(self, config):
        if 'name' in config:
            self.name = name
        if 'level' in config:
            self.set_level(level)
        if 'raise_if_exception' in config:
            self.raise_if_exception = config['raise_if_exception']
        if 'log_thread' in config:
            self.log_thread = config['log_thread']
        if 'log_multiprocessing' in config:
            self.log_multiprocessing = config['log_multiprocessing']
        if 'log_process' in config:
            self.log_process = config['log_process']
        if 'use_utc' in config:
            self.use_utc = config['use_utc']

    def set_level(self, level):
        self.level = _checkLevel(level)

    def add_handler(self, handler):
        with self._lock:
            if handler not in self.handlers:
                self.handlers.append(handler)

    def remove_handler(self, handler):
        with self._lock:
            if handler in self.handlers:
                self.handlers.remove(handler)

    def _try_log(self, level, msg, args):
        # print('_try_log')
        if not self.should_output(level):
            return
        filename, function, lineno = get_caller_info()
        # print(filename, function, lineno)
        pathname = os.path.abspath(filename)
        record = LogRecord(name=self.name, 
                           level=level, 
                           pathname=pathname, 
                           funcname=function,
                           lineno=lineno, 
                           msg=msg, args=args,
                           raise_if_exception=self.raise_if_exception,
                           log_thread=self.log_thread,
                           log_multiprocessing=self.log_multiprocessing,
                           log_process=self.log_process,
                           use_utc=self.use_utc)
        # print(record.__dict__)
        self.handle(record)

    def handle(self, record):
        for handler in self.handlers:
            handler.handle(record)

    def should_output(self, level):
        if level >= self.level:
            return True
        return False

    def log(self, level, msg, *args):
        if not isinstance(level, int):
            if self.raise_if_exception:
                raise TypeError("level must be an integer")
            else:
                return

        if self.should_output(level):
            self._log(level, msg, args)

    def debug(self, msg, *args):
        self._try_log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._try_log(INFO, msg, args)

    def warning(self, msg, *args):
        self._try_log(WARNING, msg, args)

    def error(self, msg, *args):
        self._try_log(ERROR, msg, args)

    def critical(self, msg, *args):
        self._try_log(CRITICAL, msg, args)

    fatal = critical
