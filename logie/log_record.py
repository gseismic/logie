import os
import sys
import time
import datetime
import threading
from ._level import getLevelName


class LogRecord(object):

    #__slots__ = ['name', 'level', 'level_name', 'pathname',
    #             'filename', 'module', 'func_name', 'lineno', 
    #             'msg', 'args', 'thread_name',
    #             'process', 'process_name']

    def __init__(self, name, level, 
                 pathname, funcname, lineno, 
                 msg, args,
                 raise_if_exception, log_thread, 
                 log_multiprocessing, log_process,
                 use_utc=False):
        '''
        Args:
            name: logger name
            level: msg level
            pathname: 日志info/debug/...所在文件
            lineno: 
            msg: message
            args: args of `msg`
        '''
        if use_utc:
            self._datetime = datetime.datetime.utcnow()
        else:
            self._datetime = datetime.datetime.now()
        self.name = name
        self.level = level
        self.level_name = getLevelName(level)
        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except (TypeError, ValueError, AttributeError):
            self.filename = pathname
            self.module = "Unknown module"

        self.func_name = funcname
        self.lineno = lineno
        self.msg = msg
        self.args = args

        if log_thread:
            # self.thread = threading.get_ident()
            self.thread_name = threading.current_thread().name
        else: # pragma: no cover
            # self.thread = None
            self.thread_name = threading.current_thread().name

        if not log_multiprocessing: # pragma: no cover
            self.processName = None
        else:
            self.process_name = 'MainProcess'
            mp = sys.modules.get('multiprocessing')
            if mp is not None:
                # Errors may occur if multiprocessing has not finished loading
                # yet - e.g. if a custom import hook causes third-party code
                # to run when multiprocessing calls import. See issue 8200
                # for an example
                try:
                    self.process_pame = mp.current_process().name
                except Exception: #pragma: no cover
                    pass

        if log_process and hasattr(os, 'getpid'):
            self.process = os.getpid()
        else:
            self.process = None

    def get_message(self):
        """
        Return the message for this LogRecord after merging any user-supplied
        arguments with the message.
        """
        msg = str(self.msg)
        if self.args:
            msg = msg % self.args
        return msg
