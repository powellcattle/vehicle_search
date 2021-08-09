# main.py
import re

from bs4 import BeautifulSoup

html = 'https://classiccars.com/listings/find/1940-1949?auction=false&country=united-states&dealer=true&description=truck&price-max=20000&price-min=1000&private=true&ps=60&s=datelisted&sa=true'
DATA_DIR = './meta-data/'

with open('test.html', 'r') as f:
    html = f.read()

# html = urlopen(html)
bs = BeautifulSoup(html, 'html.parser')
detail_list = bs.find_all(attrs={'class': re.compile(r'flexbox fx-justify w100 fx-va-center h-30px pad-r-md')})

counter = 0

for detail in detail_list:
    content = detail.contents[1]
    tag = content.contents[1]
    url = 'https://classiccars.com' + tag.get('href')
    name = tag.get('title')

    content = detail.contents[3]
    price = content.contents[1].getText().strip('\n')

    print(name)
    print(price)
    print(url)
