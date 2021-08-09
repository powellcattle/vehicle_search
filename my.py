import logging
import logging.config

from utils.helper import configure_logger


def foo1() :
    alog.debug("foo1 message ")

alog = configure_logger('vehicle_search', '../reports/my.log')
foo1()
alog.debug('debug message!')
alog.info('info message!')
alog.error('error message')
alog.critical('critical message')
alog.warning('warning message')
