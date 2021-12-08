import urllib.request

import requests
from bs4 import BeautifulSoup

url = 'https://classiccars.com/listings/find/1971-1987?auction=false&country=united-states&dealer=true&description=truck&price-max=15000&price-min=1000&private=true&ps=60&s=datelisted&sa=true'
proxy_dict = {'http': '3.82.162.161:49205',
              'https': '3.82.162.161:49205'}

proxy_handler = urllib.request.ProxyHandler(proxies=proxy_dict)
opener = urllib.request.build_opener(proxy_handler)
opener.addheaders = [('User-Agent','Mozilla/5.0')]
urllib.request.install_opener(opener)
page = urllib.request.urlopen(url)
pass
