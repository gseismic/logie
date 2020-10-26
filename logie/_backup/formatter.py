
# from logging
class PercentStyle(object):

    # default_format = '%(message)s'
    default_format = "[%(asctime)s][%(levelname)s]: %(name)s: %(message)s"
    asctime_format = '%(asctime)s'
    asctime_search = '%(asctime)'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format

    def usesTime(self):
        return self._fmt.find(self.asctime_search) >= 0

    def format(self, record):
        return self._fmt % record.__dict__


class StringTemplateStyle(PercentStyle):
    default_format = '${message}'
    asctime_format = '${asctime}'
    asctime_search = '${asctime}'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format
        self._tpl = Template(self._fmt)

    def usesTime(self):
        fmt = self._fmt
        return fmt.find('$asctime') >= 0 or fmt.find(self.asctime_format) >= 0

    def format(self, record):
        return self._tpl.substitute(**record.__dict__)


BASIC_FORMAT = "[%(asctime)s][%(levelname)s]: %(name)s: %(message)s"

_STYLES = {
    '%': (PercentStyle, BASIC_FORMAT),
    '{': (StrFormatStyle, '[{asctime}][{levelname}]: {name}: {message}'),
    '$': (StringTemplateStyle, '[${asctime}][${levelname}]: ${name}: ${message}')
}

