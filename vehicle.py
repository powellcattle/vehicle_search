from craigslist.base import CraigslistBase


class CraigslistVehicle(CraigslistBase):
    """ Craigslist for sale wrapper. """

    default_category = 'cta'
    custom_result_fields = True

    extra_filters = {
        'searchNearby': {'url_key': 'searchNearby', 'value': None},
        'postedToday': {'url_key': 'postedToday', 'value': None},
        'srchType': {'url_key': 'srchType', 'value': None},
        'hasPic': {'url_key': 'hasPic', 'value': None},
        # price
        'min_price': {'url_key': 'min_price', 'value': None},
        'max_price': {'url_key': 'max_price', 'value': None},
        # make and model
        'make': {'url_key': 'auto_make_model', 'value': None},
        'model': {'url_key': 'auto_make_model', 'value': None},
        # model year
        'min_year': {'url_key': 'min_auto_year', 'value': None},
        'max_year': {'url_key': 'max_auto_year', 'value': None},
        # odometer
        'min_miles': {'url_key': 'min_auto_miles', 'value': None},
        'max_miles': {'url_key': 'max_auto_miles', 'value': None},
        # engine displacement (cc)
        'min_engine_displacement': {
            'url_key': 'min_engine_displacement_cc', 'value': None},
        'max_engine_displacement': {
            'url_key': 'max_engine_displacement_cc', 'value': None},
    }

    def customize_result(self, result):
        for attr in result.get('attrs', []):
            attr_lower = attr.lower()
            # Get miles.
            if attr_lower.startswith('odometer: '):
                result['miles'] = attr[10:]
            # Get engine displacement
            if attr_lower.startswith('engine displacement (cc): '):
                result['engine_displacement'] = attr[26:]