

class TimedRotatingFileHandler(FileHandler):
    '''
        handler = TimedRotatingFileHandler(
            '/var/log/foo.log',
            date_format='%Y-%m-%d',
            rollover_format='{basename}{ext}.{timestamp}')
    '''
    pass
