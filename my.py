import urllib.parse
from urllib.parse import urlparse

cl = 'https://classics.autotrader.com/classic-cars-for-sale/classic_trucks-for-sale?'
filters = {
    'year_from': 1940,
    'year_to': 1949,
    'price_from': 1000,
    'price_to': 30000,
    'limit': 500,
    'order': 'created desc',
    'distance': 'nationwide'}

print(cl + urllib.parse.urlencode(filters))
