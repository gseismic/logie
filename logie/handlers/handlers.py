
class Handler(object):
    time_formatter = "%Y-%m-%d %H:%M:%S.%f"
    # def __init__(self, tag):
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
