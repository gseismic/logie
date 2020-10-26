import logie
# import logging as logie

# https://www.machinelearningplus.com/python/python-logging-guide/
# Gets or creates a logger
logger = logie.getLogger(__name__)
# set log level
logger.setLevel(logie.WARNING)

# define file handler and set formatter
file_handler = logie.FileHandler('logfile.log')
formatter = logie.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

# Logs
logger.debug('A debug message')
logger.info('An info message')
logger.warning('Something is not right.')
logger.error('A Major error has happened.')
logger.critical('Fatal error. Cannot continue')
