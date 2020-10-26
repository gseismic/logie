import time
from ._level import NOTSET, DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
from .colored import colored


class FormatStyle(object):

    def format(self, record):
        raise NotImplementedError()


class StrFormatStyle(FormatStyle):
    default_format = '[{datetime}] {level_name}: {name}: {message}'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format

    def format(self, record):
        return self._fmt.format(**record.__dict__)


class Formatter(object):
    default_date_format = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, fmt=None, datefmt=None):
        self.fmt = fmt 
        self.datefmt = datefmt or self.default_date_format
        self._style = StrFormatStyle(fmt)

    def format_time(self, dt, datefmt=None):
        return dt.strftime(datefmt)

    def format(self, record):
        record.datetime = self.format_time(record._datetime, self.datefmt)
        record.message = record.get_message()
        return self._style.format(record)


class ColoredFormatter(Formatter):

    def format(self, record):
        s = Formatter.format(self, record)
        if record.level == DEBUG:
            s = colored(s, fore='yellow')
        elif record.level == INFO:
            s = s
        elif record.level == WARNING:
            s = colored(s, fore='purple')
        elif record.level == ERROR:
            s = colored(s, fore='red')
        elif record.level == CRITIAL:
            s = colored(s, fore='red', back='white')
        return s


_default_colored_formatter = ColoredFormatter()
_default_formatter = Formatter()


if __name__ == '__main__':
    if 1:
        formatter = Formatter()
        # formatter.format(record)
