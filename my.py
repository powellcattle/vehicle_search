import cloudscraper
import json
import sys
from bs4 import BeautifulSoup

f = open('./test.html',encoding='utf8')
html = f.read()
f.close()
# https://classics.autotrader.com/classic-cars-for-sale/classic_trucks-ford-for-sale?year_from=1940&year_to=1970&price_to=20000&seller_type=seller&limit=500&order=created+desc&distance=nationwide

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
soup = BeautifulSoup(html,'html.parser')

jobject = soup.find_all(attrs={"class":"details"})
for item in jobject:

    print(item)
# pass
# start_json = html.find("<script type='application/ld+json'>") + len("<script type='application/ld+json'>")
# end_json = html.find("</script", start_json)
# print(html[start_json:end_json])


#
#
# html = list(soup.children)
#
pass
#
# for item in (soup.children)
#     print(item)