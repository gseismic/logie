from .logger import Logger
from ._level import NOTSET
from .handlers import StreamHandler


_logger_dict = {}
_pending_logger_config = {}


# def get_logger(name, add_console_if_not_exist=True)
def get_logger(name):
    '''
    如果logger `name` 存在，则调用
    如果不存在，则创建并保存
    '''
    if name in _logger_dict:
        logger = _logger_dict[name]
    else:
        logger = Logger(name)
        _logger_dict[name] = logger

    if name in _pending_logger_config:
        logger.update_config(_pending_logger_config[name])
        del _pending_logger_config[name]

    return logger


def config_logger(name='root', 
                  level=NOTSET, 
                  raise_if_exception=True, 
                  log_thread=True,
                  log_multiprocessing=True,
                  log_process=True,
                  use_utc=False):
    '''
    如果logger `name` 存在，则配置
    如果不存在，则保存，将来配置
    '''
    config = {
        'level': level,
        'raise_if_exception': raise_if_exception,
        'log_thread': log_thread,
        'log_multiprocessing': log_multiprocessing,
        'log_process': log_process,
        'use_utc': use_utc
    }
    if name not in _logger_dict:
        _pending_logger_config[name] = config
    else:
        _logger_dict[name].update_config(config)
