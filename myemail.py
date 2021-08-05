import logging

# main.py
import os
import sys


def _init_logger():
    logger = logging.getLogger('vehicle_search')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s: %(levelname)s: %(name)s: %(module)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


_init_logger()

_logger = logging.getLogger('vehicle_search')
_logger.info('Application started in %s', os.getcwd())
