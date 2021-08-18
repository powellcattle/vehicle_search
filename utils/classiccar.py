import json
import logging
import sys

from utils.vehiclesearchbase import VehicleSearchBase

_logger = logging.getLogger('vehicle_search')

try:
    f = open("meta-data/craigsliststates.json")
    STATE_SITES = json.load(f)
    f.close()
except OSError as e:
    _logger.error(e)
    sys.intern(e.strerror)


class ClassicCar(VehicleSearchBase) :
    base_filters =  {
        'auction': {'url_key': 'auction', 'value': False},
        'country': {'url_key': 'country', 'value': 'united-states'},
        'dealer': {'url_key': 'dealer', 'value': True},
        'private': {'url_key': 'private', 'value': True},
        'ps': {'url_key': 'ps', 'value': 60},
        's': {'url_key': 's', 'value': 'datelisted'},
        'sa': {'url_key': 'sa', 'value': True}
    }

