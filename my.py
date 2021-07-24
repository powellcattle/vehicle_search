from urllib.request import urlopen
import re

import bs4.element
from bs4 import BeautifulSoup

html = 'https://cars.oodle.com/1940_1949-multiple-multiple/el-campo-tx/antique-classic-cars/condition_used/has_photo_thumbnail/make_chevrolet/make_ford/make_international/make_studebaker/model_panel_truck/model_pick_up/model_pickup/price_1000_20000/?s=date&inbs=1&r=country'



html = urlopen(html)
bs = BeautifulSoup(html, 'html.parser')
pattern = re.compile('\sfor\s\$')
detail_list = bs.find_all('div', {'class':'action-wrapper'})
for detail in detail_list:
    for content in detail.contents:
        if type(content) == bs4.element.Tag :
            tag = content.contents[3].contents[1]
            href = tag['href']
            print(href)
            txt = tag.getText()
            x = pattern.search(txt)
            title = txt[0:x.regs[0][0]]
            print(title)
            price = txt[x.regs[0][1]-1:]
            print(price)



