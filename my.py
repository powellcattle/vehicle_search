from urllib.request import urlopen

import cloudscraper
import json
import sys
from bs4 import BeautifulSoup

f = open('./test.html', encoding='utf8')
html = f.read()
f.close()
html = urlopen('https://classics.autotrader.com/classic-cars-for-sale/classic_trucks-for-sale?year_from=1940&year_to=1970&price_to=20000&seller_type=seller&limit=500&order=created+desc&distance=nationwide')



# try:
#     f = open("./test.json")
#     search_names_json = json.load(f)
#     f.close()
# except OSError as e:
#     sys.intern(e)


# for item in search_names_json:
#     if item.get('@type').lower() == 'car':
#         description = item.get('description')
#         offers = item.get('offers')
#         price = offers.get('price')
#         seller = offers.get('seller')
#         url = offers.get('url')
#         pass


#  <div class="details">
#

all_results = list(dict())

try:
    bs = BeautifulSoup(html, 'html.parser')
    detailList = bs.find_all('div', {'class': 'details'})
    for detail in detailList:
        detail_dict = dict()
        details_html = detail.find('a', {'class': 'name'}, href=True)
        urlLink = details_html['href']
        print(urlLink)
        name = detail.find('h3', {'class': 'model'})
        print(name.getText())
        price = detail.find('h4', {'class': 'price'})
        print(price.getText())
        all_results.append(
                {'name': name,
                 'url': urlLink,
                 'price': price})


except AttributeError as e:
    print(e)
    sys.exit(-1)

