import logie
import time


import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s')

if 0:
    logger = logging.getLogger()
    cnt = 10000
    t0 = time.time()
    while cnt > 0:
        logger.info('info msg %d', cnt)
        cnt -= 1
    print((time.time() - t0)/10000)

logger = logie.Logger()
# logger = logie.Logger(log_process=False, log_multiprocessing=False)

h1 = logie.StreamHandler('INFO')
logger.add_handler(h1)

#logger.debug('debub msg')
if 1:
    t0 = time.time()
    cnt = 10000
    while cnt > 0:
        logger.info('info msg %d', cnt)
        cnt -= 1

    print((time.time() - t0)/10000)
    # logger.warning('warning msg')
    # logger.error('error msg')

