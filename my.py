from urllib.request import urlopen
import re

import bs4.element
from bs4 import BeautifulSoup

html = '1947 Dodge Power Wagon'
html1 = '1948 Dodge Power Wagon'

if re.compile(r'\b({0})\b'.format(html), flags=re.IGNORECASE).search(html1):
    print(True)
else:
    print(False)





