# encoding: utf8
import sys, os
import codecs
import time, datetime
import socket
from collections import defaultdict
from .colored import colored

"""
注意：
    logbook use lpush/..., not publish, it's reasonable!
    or, you will miss messages, which should not happen

So, Use logbook directly, its source code is beautiful!
"""


DEBUG       = -1
INFO        = 0
LOG         = 2
NOTICE      = 2  # 2019-03-17 05:57:15 new
WARNING     = 3
ERROR       = 4
CRITICAL    = 5


class Handler(object):

    time_formatter = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, tag, level=DEBUG):
        # level: added
        self.tag = tag.upper()
        self.level = level
        self.hostname = socket.gethostname()

    def __call__(self, now, name, msg, head=True, wait=0):
        raise NotImplemented

    def progress_wait(self, wait_sleep, num_intervals=10, sep='.', twice=True):
        t = datetime.datetime.now()
        interval = wait_sleep/float(num_intervals)
        remaining = wait_sleep
        told = False
        sys.stdout.write(' ### waiting {}(sec) '.format(remaining))
        while num_intervals > 0:
            num_intervals -= 1
            remaining -= interval
            if twice and not told and remaining < 3.2:
                sys.stdout.write('[R=%.2f]' % (remaining))
                told = True
            sys.stdout.write(sep)
            sys.stdout.flush()
            time.sleep(interval)
        sys.stdout.write('\n')
        sys.stdout.flush()
        #print((datetime.datetime.now() - t).total_seconds())


class StreamHandler(Handler):

    def __init__(self, *args, **kwargs):
        Handler.__init__(self, *args, **kwargs)

    def __call__(self, now, name, msg, head=True, wait=0):
        if head == True:
            head = "[%s][%s][%s]: " % (now.strftime(self.time_formatter), self.tag, name)
            _message = head + "%s" % msg
        else:
            _message = msg
        if wait <= 0:
            print(_message)
        else:
            sys.stdout.write(_message)
            sys.stdout.flush()
            self.progress_wait(wait)


class ColoredStreamHandler(Handler):

    def __init__(self, tag_color=None, body_color=None, style='', *args, **kwargs):
        Handler.__init__(self, *args, **kwargs)
        default_tag_color = dict(back='yellow', fore='', style='')
        default_body_color = dict(back='', fore='red', style='')
        _default_color = dict(back='', fore='', style='')
        # tag_color 可能有部分关键字缺
        from copy import copy
        if tag_color != None: 
            _c = _default_color.copy()
            _c.update(tag_color)
            self.tag_color = _c
        else: self.tag_color = default_tag_color
        if body_color != None: 
            _c = _default_color.copy()
            _c.update(body_color)
            self.body_color = _c
        else: self.body_color = default_body_color

    def __call__(self, now, name, msg, head=True, wait=0):
        if head == True:
            head = "[%s][%s][%s]: " %(
                        now.strftime(self.time_formatter), 
                        colored(self.tag, **self.tag_color), name)
            _message = head + "%s" % colored(msg, **self.body_color)
        else:
            _message = colored(msg, **self.body_color)
        if wait <= 0:
            print(_message)
        else:
            sys.stdout.write(_message)
            sys.stdout.flush()
            self.progress_wait(wait)


class FileHandler(Handler):
    """ 每天的日记，可以通过定时程序实现
    info, error, debug单独文件，方便检查
    """
    def __init__(self, logname, logdir, bydate=False, separated_log=True, *args, **kwargs):
        """
        separated_log = True, 方便删除不重要的日记，比如debug
        """
        super(FileHandler, self).__init__(*args, **kwargs)
        self.logname = logname
        self.logdir = logdir
        self.bydate = bydate
        self.separated_log = separated_log
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.path = os.path.join(logdir, logname)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def __call__(self, now, name, msg, head=True, wait=0):
        if head == True:
            head = "[%s][%s][%s]: " % (now.strftime(self.time_formatter), self.tag, name)
            _message = head + "%s" % msg
        else:
            _message = msg
        if wait > 0:
            time.sleep(wait)

        if not self.bydate:
            self.logfile = os.path.join(self.path, '%s.%s.log' % (now.strftime("%Y-%m-%d"), self.tag))
        else:
            self.logfile = os.path.join(self.path, '%s.log' % self.tag)

        with codecs.open(self.logfile, 'a', encoding='utf8') as f:
            f.write('%s\n' % str(_message))
        # fileutil.append2file(str(_message)+'\n', self.logfile)



default_debug_console_color     = {'tag_color':dict(back='blue', fore='', style=''), 
                                   'body_color':dict(back='', fore='blue', style='')}
default_info_console_color     = {'tag_color':dict(back='', fore='', style=''), 
                                   'body_color':dict(back='', fore='white', style='')}
default_log_console_color       = {'tag_color':dict(back='white', fore='yellow', style=''), 
                                   'body_color':dict(back='', fore='cyan', style='')}
default_warning_console_color   = {'tag_color':dict(back='yellow', fore='', style=''), 
                                   'body_color':dict(back='', fore='yellow', style='')}
default_error_console_color     = {'tag_color':dict(back='red', fore='', style=''), 
                                   'body_color':dict(back='', fore='red', style='')}
default_critical_console_color  = {'tag_color':dict(back='red', fore='', style=''), 
                                   'body_color':dict(back='red', fore='white', style='')}

def get_logger(
                 logname=None, 
                 logdir=None,
                 bydate=False,
                 separated_log=True,
                 level=DEBUG,
                 console_log=True,      # 默认所有开启屏幕打印
                 debug_log=False,       # debug 是否写入文件
                 info_log=False,        # info 是否打印文件
                 log_log=True,          # log 是否打印文件
                 report_log=True,       # report 是否打印文件, 正常的信息，需要文件记录，但不是警告
                 warn_log=True,         # warn 是否写入文件
                 error_log=True,        # error 是否写入文件
                 critical_log=True,     # critical to file
                 debug_console_color=default_debug_console_color.copy(),
                 info_console_color=default_info_console_color.copy(),
                 log_console_color=default_log_console_color.copy(),
                 warning_console_color=default_warning_console_color.copy(),
                 error_console_color=default_error_console_color.copy(),
                 critical_console_color=default_critical_console_color.copy(),
                 ):
    #2017-04-09 17:20:02 added
    if logname is None:
        logname = "main"
    if logdir is None:
        logdir = "log"
    log_handlers = defaultdict(list)
    if console_log:
        log_handlers['debug_handlers'].append( ColoredStreamHandler(tag="debug", **debug_console_color))
        #log_handlers['info_handlers'].append( StreamHandler(tag="info"))
        log_handlers['info_handlers'].append( ColoredStreamHandler(tag="info", **info_console_color))
        log_handlers['log_handlers'].append( ColoredStreamHandler(tag="log", **log_console_color))
        log_handlers['warn_handlers'].append( ColoredStreamHandler(tag="warn", **warning_console_color))
        log_handlers['error_handlers'].append( ColoredStreamHandler(tag="error", **error_console_color))
        log_handlers['critical_handlers'].append( ColoredStreamHandler(tag="critical", **critical_console_color))
    logmask_dic = {'debug':debug_log, 'info':info_log, 'log':log_log, 
                   'warn':warn_log, 'error':error_log, 'critical':critical_log}
    for key in logmask_dic:
        if logmask_dic[key]:
            # bydate added
            log_handler = FileHandler(logname, logdir, tag=key, bydate=bydate,
                    separated_log=separated_log)
            log_handlers[key+'_handlers'].append(log_handler)
    _logger = Logger(logname=logname, logdir=logdir, level=level, **log_handlers)
    return _logger


class Logger(object):

    max_wait = 3
    __num_msg = defaultdict(int)
    def __init__(self, 
                 logname="main", 
                 logdir="log",
                 level=DEBUG,
                 max_wait=60*3,
                 debug_handlers=None,
                 info_handlers=None,
                 log_handlers=None,
                 warn_handlers=None,
                 error_handlers=None,
                 critical_handlers=None):
        self.logname = logname
        self.logdir = logdir
        level_dict = {'DEBUG': DEBUG, 'INFO': INFO, 'WARNING': WARNING, 'ERROR': ERROR, 'CRITICAL': CRITICAL}
        if isinstance(level, str):
            self.level = level_dict.get(level.upper())
            if self.level is None:
                print('Warning: Invalid level %s, using `INFO` level ...' % str(level))
                self.level = INFO
        else:
            self.level = level
        self.max_wait = max_wait
        self.log_handlers = defaultdict(list)
        # debug
        if debug_handlers is None:
            self.log_handlers['debug'] = [
                    ColoredStreamHandler(tag="debug", **default_debug_console_color.copy())
                    ]
        else: self.set_log_handlers('debug', debug_handlers)
        # info
        if info_handlers is None:
            self.log_handlers['info'] = [StreamHandler("info")]
        else: self.set_log_handlers('info', info_handlers)
        # log 
        if log_handlers is None:
            self.log_handlers['log'] = [
                    ColoredStreamHandler(tag="log", **default_log_console_color.copy()),
                    FileHandler(logname, logdir, tag="log")]
        else: self.set_log_handlers('log', log_handlers)
        # warning
        if warn_handlers is None:
            self.log_handlers['warn'] = [
                    ColoredStreamHandler(tag="warn", **default_warning_console_color.copy()),
                    FileHandler(logname, logdir, tag="warn")]
        else: self.set_log_handlers('warn', warn_handlers)
        if error_handlers is None:
            self.log_handlers['error'] = [
                    ColoredStreamHandler(tag="error", **default_error_console_color.copy()),
                    FileHandler(logname, logdir, tag="error")]
        else: self.set_log_handlers('error', error_handlers)
        if critical_handlers is None:
            self.log_handlers['critical'] = [
                    ColoredStreamHandler(tag="critical", **default_critical_console_color.copy()),
                    FileHandler(logname, logdir, tag="critical")]
        else: self.set_log_handlers('critical', critical_handlers)

    def set_log_handlers(self, key, log_handlers):
        if isinstance(log_handlers, (list,tuple,set)):
            self.log_handlers[key] = list(log_handlers)
        else:
            self.log_handlers[key] = [log_handlers]

    def set_level(self, level):
        self.level = level

    def set_verbosity(self, verbosity=1):
        raise

    def set_max_wait(self, wait):
        self.max_wait = wait

    def _log(self, key, message, head=True, wait=0, sound=False):
        now = datetime.datetime.now()
        if wait > self.max_wait:
            wait = self.max_wait
        if sound:
            from sound import sound_warning
            sound_warning()
        for handler in self.log_handlers[key]:
            handler(now=now, name=self.logname, msg=message, head=head, wait=wait)
            wait = 0

    def debug(self, message, head=True, wait=0, sound=False):
        tag = 'debug'
        self.__num_msg[tag] += 1
        if self.level <= DEBUG:
            self._log(tag, message, head, wait=wait, sound=sound)

    def info(self, message, head=True, wait=0, sound=False):
        tag = 'info'
        self.__num_msg[tag] += 1
        if self.level <= INFO:
            self._log(tag, message, head, wait=wait, sound=sound)

    def log(self, message, head=True, wait=0, sound=False):
        tag = 'log'
        self.__num_msg[tag] += 1
        if self.level <= LOG:
            self._log(tag, message, head, wait=wait, sound=sound)

    def warning(self, message, head=True, wait=0, sound=False):
        self.warn(message, head, wait, sound)

    def warn(self, message, head=True, wait=0, sound=False):
        tag = 'warn'
        self.__num_msg[tag] += 1
        if self.level <= WARNING:
            self._log(tag, message, head, wait=wait, sound=sound)

    def error(self, message, head=True, wait=0, sound=False):
        tag = 'error'
        self.__num_msg[tag] += 1
        if self.level <= ERROR:
            self._log(tag, message, head, wait=wait, sound=sound)

    def critical(self, message, head=True, wait=0, sound=False):
        tag = 'critical'
        self.__num_msg[tag] += 1
        if self.level <= CRITICAL:
            self._log(tag, message, head, wait=wait, sound=sound)
            raise Exception('Critical Error: %s' % message)

    def num_msgs(self, tag=None):
        if tag.lower() in ['debug', 'info', 'log', 'warn', 'error', 'critial']:
            return self.__num_msg[tag.lower()]
        elif tag is None:
            total = 0
            for tag in self.__num_msg:
                total += self.__num_msg[tag]
            return total
        else:
            return self.__num_msg[tag.lower()]

    def num_debugs(self):
        return self.num_msgs(tag='debug')

    def num_infos(self):
        return self.num_msgs(tag='info')

    def num_logs(self):
        return self.num_msgs(tag='log')

    def num_warns(self):
        return self.num_msgs(tag='warn')

    def num_errors(self):
        return self.num_msgs(tag='error')

    def num_criticals(self):
        return self.num_msgs(tag='critical')

    def post_url(self, message, head=True):
        pass



if __name__ == "__main__":
    url = "http://www.baidu.com"
    log = Logger(logname="main")
    log.debug("logger self testing...")
    log.info("logger self testing...")
    log.log("logger self testing...")
    log.warning("logger self testing...")
    log.error("logger self testing...")
    try:
        log.critical("logger self testing...")
    except Exception as e:
        print(e)
    print('-----------------')
    log2 = get_logger("main2", log_log=True, bydate=True)
    log2.set_level(INFO)
    log2.set_level(DEBUG)
    log2.debug("logger self testing...")
    log2.info("logger self testing...")
    log2.log("Log logger self testing...")
    log2.warning("logger self testing...")
    log2.error("logger self testing...")
    print(log2.num_warns())
    sys.exit()
    try:
        log2.critical("logger self testing...")
    except Exception as e:
        print(e)

    log2.error("logger self testing..0", head=False)
    log2.info("logger self testing...0", head=False)
    #log2.info("logger self testing...0", wait=3)
    log2.debug("logger self testing...10", wait=1)
    log2.debug("logger self testing...10", wait=3)
    log2.warning("logger self testing...10", wait=3)
    log2.warning("logger self testing...10", wait=15)
    print(log2.num_warns())
    sys.exit()
