import logie
import time


logger = logie.Logger()

h1 = logie.StreamHandler(level='INFO')
logger.add_handler(h1)
h1 = logie.ColoredStreamHandler(level='debug')
logger.add_handler(h1)
f1 = logie.FileHandler(filename='logie.log')
logger.add_handler(f1)

logger.debug('debug msg')
logger.info('info msg %d', 3)
logger.warning('warning msg')
logger.error('error msg')
