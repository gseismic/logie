from logie import get_logger, config_logger


logger1 = get_logger('main')
logger2 = get_logger('main')


print(logger1, logger2)
logger1.debug('debub msg')
logger1.info('info msg')
logger1.warning('warning msg')
logger1.error('error msg')

