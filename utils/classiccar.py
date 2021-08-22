from collections import namedtuple

import requests
from requests import RequestException, utils

try:
    from urlparse import urljoin  # PY2
except ImportError:
    from urllib.parse import urljoin  # PY3

Results = namedtuple('Results', ['all', 'sorted'])
USER_AGENT = 'Mozilla/5.0'


class ClassicCar(object):
    url_template = 'https://classiccars.com/listings/find/'
    url_year = '%(year_from)s-%(year_to)s/'

    base_filters = {
        'auction': False,
        'country': 'united-states',
        'dealer': False,
        'description': 'truck',
        'price-min': None,
        'price-max': None,
        'private': True,
        'ps': 60,
        's': 'datelisted',
        'sa': True
    }

    extra_filters = {}
    results = Results(list(dict()), list(dict()))

    def __init__(self, year_from=None, year_to=None, make=None, filters=None):
        if year_from and year_to:
            self.url_year = self.url_year % {'year_from': year_from, 'year_to': year_to}
            self.url_template += self.url_year
        if make:
            self.url_template += self.url_template + '/' + make

        self.set_filters(filters)

    def set_filters(self, filters):
        for key, value in (filters or {}).items():
            self.base_filters[key] = value

    @staticmethod
    def requests_get(*args, **kwargs):

        kwargs.setdefault('headers', {}).setdefault('User-Agent', USER_AGENT)

        try:
            return requests.get(*args, **kwargs)
        except RequestException as exc:
            # if logger:
            #     logger.warning('Request failed (%s). Retrying ...', exc)
            return requests.get(*args, **kwargs)

    def get_results(self):

        while True:
            response = ClassicCar.requests_get(self.url_template, params=self.base_filters)
            # self.logger.info('GET %s', response.url)
            # self.logger.info('Response code: %s', response.status_code)
            # response.raise_for_status()  # Something failed?

            soup = utils.bs(response.content)
            # if not total:
            #     total = self.get_results_approx_count(soup=soup)

            rows = soup.find('ul', {'class': 'rows'})
            for row in rows.find_all('li', {'class': 'result-row'},
                                     recursive=False):
                # if limit is not None and results_yielded >= limit:
                #     break
                # self.logger.debug('Processing %s of %s results ...',
                #                   total_so_far + 1, total or '(undefined)')

                yield self.process_row(row)
            #
            #     results_yielded += 1
            #     total_so_far += 1
            #
            # if results_yielded == limit:
            #     break
            # if (total_so_far - start) < RESULTS_PER_REQUEST:
            #     break
            # start = total_so_far

    def process_row(self, row):
        id = row.attrs['data-pid']
        repost_of = row.attrs.get('data-repost-of')

        link = row.find('a', {'class': 'hdrlnk'})
        name = link.text
        url = urljoin(self.url, link.attrs['href'])

        time = row.find('time')
        if time:
            datetime = time.attrs['datetime']
        else:
            pl = row.find('span', {'class': 'pl'})
            datetime = pl.text.split(':')[0].strip() if pl else None
        price = row.find('span', {'class': 'result-price'})
        where = row.find('span', {'class': 'result-hood'})
        if where:
            where = where.text.strip()[1:-1]  # remove ()
        tags_span = row.find('span', {'class': 'result-tags'})
        tags = tags_span.text if tags_span else ''

        result = {'id': id,
                  'name': name,
                  'url': url,
                  'last_updated': datetime,
                  'price': price.text if price else None,
        }

        return result