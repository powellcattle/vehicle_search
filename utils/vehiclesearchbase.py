from collections import namedtuple

try:
    from urlparse import urljoin  # PY2
except ImportError:
    from urllib.parse import urljoin  # PY3

Results = namedtuple('Results', ['all', 'sorted'])


class VehicleSearchBase(object):
    """ Base class for all Vehicle Search Classes """
    default_year_from = 1940
    default_year_to = 1987
    default_price_min = 1000
    default_price_max = 30000
    extra_filters = {}
    results = Results(list(dict()), list(dict()))

    base_filters = {
        'auction': {'url_key': 'auction', 'value': False},
        'country': {'url_key': 'country', 'value': 'united-states'},
        'dealer': {'url_key': 'dealer', 'value': True},
        'private': {'url_key': 'private', 'value': True},
        'ps': {'url_key': 'ps', 'value': 60},
        's': {'url_key': 's', 'value': 'datelisted'},
        'sa': {'url_key': 'sa', 'value': True}
    }

    def __init__(self, year_from=None, year_to=None, price_min=None, price_max=None, filters=None):

        self.year_from = year_from or self.default_year_from
        self.year_to = year_to or self.default_year_to
        if self.year_from > self.year_to:
            msg = 'From year must be greater than to year'
            raise ValueError(msg)

        self.price_min = price_min or self.default_price_min
        self.price_max = price_max or self.default_price_max

        self.filters = self.get_filters(filters)

    def get_filters(self, filters):

        """Parses filters passed by the user into GET parameters."""

        # list_filters = self.get_list_filters(self.url)

        # If a search has few results, results for "similar listings" will be
        # included. The solution is a bit counter-intuitive, but to force this
        # not to happen, we set searchNearby=True, but not pass any
        # nearbyArea=X, thus showing no similar listings.
        parsed_filters = {}

        for key, value in (filters or {}).items():
            try:
                filter_ = self.base_filters.get(key) or self.extra_filters.get(key)
                if filter_['value'] is None:
                    parsed_filters[filter_['url_key']] = value
                elif isinstance(filter_['value'], dict):
                    valid_options = filter_['value']
                    # if not utils.isiterable(value) or isinstance(value, str):
                    #     value = [value]  # Force to list
                    options = []
                    for opt in value:
                        try:
                            options.append(valid_options[opt])
                        except KeyError:
                            self.logger.warning(
                                "'%s' is not a valid option for %s"
                                % (opt, key)
                            )
                    parsed_filters[filter_['url_key']] = options
                elif value:  # Don't add filter if ...=False
                    parsed_filters[filter_['url_key']] = value
            except KeyError:
                self.logger.warning("'%s' is not a valid filter", key)

        return parsed_filters


    def get_results(self):
        pass