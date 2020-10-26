from .__version__ import __version__
from .handlers import DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
from .handlers import BaseHandler, StreamHandler, FileHandler
from .handlers import ColoredStreamHandler

from .logger import Logger
from .utils import get_logger, config_logger

#def shutdown(handlerList=_handlerList):
#    pass
#import atexit
#atexit.register(shutdown)
