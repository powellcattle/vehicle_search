import logging
import logging.config

from utils.other import foo, configure_logger


# def configure_logger(name, log_path):
#     logging.config.dictConfig({
#         'version': 1,
#         'formatters': {
#             'default': {'format': '%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s:%(lineno)d]: -%(message)s',
#                         'datefmt': '%Y-%m-%d %H:%M:%S'}
#         },
#         'handlers': {
#             'console': {
#                 'level': 'DEBUG',
#                 'class': 'logging.StreamHandler',
#                 'formatter': 'default',
#                 'stream': 'ext://sys.stdout'
#             },
#             'file': {
#                 'level': 'DEBUG',
#                 'class': 'logging.handlers.RotatingFileHandler',
#                 'formatter': 'default',
#                 'filename': log_path,
#                 'maxBytes': 1024,
#                 'backupCount': 3
#             }
#         },
#         'loggers': {
#             'vehicle_handler': {
#                 'level': 'DEBUG',
#                 'handlers': ['console', 'file']
#             },
#             'module': {
#                 'level': 'DEBUG',
#                 'handlers': ['console', 'file']
#             }
#         },
#         'disable_existing_loggers': False
#     })
#     return logging.getLogger(name)

def foo1() :
    alog.debug("foo1 message ")

alog = configure_logger('vehicle_search', 'log13.txt')
foo1()
foo(logger_name='vehicle_search')
alog.debug('debug message!')
alog.info('info message!')
alog.error('error message')
alog.critical('critical message')
alog.warning('warning message')
