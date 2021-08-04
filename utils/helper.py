import json
import re
import smtplib
import ssl
import sys
import urllib
from email.message import EmailMessage
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

import bs4
from bs4 import BeautifulSoup

from utils.vehicle import CraigslistVehicle

AUTOTRADER_BASE_URL = 'https://classics.autotrader.com/classic-cars-for-sale?'
AUTOTRADER_BASE_TRUCKSONLY_URL = 'https://classics.autotrader.com/classic-cars-for-sale/classic_trucks-for-sale?'
OODLE_URL_START = 'https://cars.oodle.com'
OODLE_URL_END = '/houston-tx/antique-classic-cars/condition_used/has_photo_thumbnail/make_chevrolet/make_ford' \
                '/make_international/make_studebaker/model_panel_truck/model_pick_up/model_pickup'
oodle_pattern = re.compile('\sfor\s\$')
pager_pattern = re.compile('of\s')

stateSites = []
try:
    f = open("meta-data/sort_filters.json")
    sort_filters_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

try:
    f = open("meta-data/craigsliststates.json")
    stateSites = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

list_state_dict = stateSites.get('states')
SEARCH_LIMIT = 100


def find_whole_word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def add_nonduplicate_to_results(candidates, final_results):
    for candidate in candidates:
        url = candidate.get('url')
        name = candidate.get('name')

        for item in final_results:
            if url == item.get('url') or name == item.get('name'):
                break
        else:
            final_results.append(
                {
                    'id': candidate.get('id'),
                    'name': candidate.get('name'),
                    'url': candidate.get('url'),
                    'price': candidate.get('price')
                }
            )

    return


def type_results(results_all, results_all_typed):
    # iterate over all listing results
    for listing in results_all:
        # find all the dictionary with all the groups
        for filters_dict in sort_filters_json['filters']:
            # iterate over all the sorting groups
            for vehicle_group in filters_dict:
                # look at each alias for a given group
                for alias in filters_dict.get(vehicle_group):
                    listing_title = listing.get('name')
                    if find_whole_word(alias)(listing_title):
                        for item in results_all_typed:
                            if (item.get('url') == listing.get('url') or item.get('name') == listing_title) and \
                                    vehicle_group == item.get('vtype'):
                                break
                        else:
                            results_all_typed.append(
                                {'vtype': vehicle_group,
                                 'id': listing.get('id'),
                                 'name': listing.get('name'),
                                 'url': listing.get('url'),
                                 'price': listing.get('price')
                                 }
                            )
                        break


def write_html(results_all_typed, results_all):
    return_text = ''

    for filters_dict in sort_filters_json['filters']:

        text = ''
        for vehicle in filters_dict:
            text = '<p><table border="0" style="width: 100%; border-collapse: collapse; border-style: none;"><thead>'
            text += '<tr style="text-align: left; border-style: hidden;">'
            text += '<td style="width:10%;height:20px;border-style:hidden;"><strong>' + vehicle.upper() + '</strong>'
            text += '</td>'
            text += '</tr></thead><tbody>'

            for result in results_all_typed:
                if result.get('vtype') == vehicle:
                    text += '<tr style="border-style:none;">'
                    # text += '<td style="width:10%;border-style:none;">' + result.get('price') + '</td>'
                    text += '<td style="width:10% border-style:none;">'
                    text += '<a href="' + result.get('url') + '"title="' + result.get('name') + '"target="_blank">'
                    text += '[' + result.get('price') + ']  ' + result.get('name') + '</a>'
                    text += '</td>'
                    text += '</tr>'
            text += '</table>'
            text += '</p>'

        return_text += text

    text = '<p><table border="0" style="width: 100%; border-collapse: collapse; border-style: none;"><thead>'
    text += '<tr style="text-align: left; border-style: hidden;">'
    text += '<td style="width:10%;height:20px;border-style:hidden;"><strong>ALL VEHICLES</strong>'
    text += '</td>'
    text += '</tr></thead><tbody>'

    for result in results_all:
        text += '<tr style="border-style:none;">'
        # text += '<td style="width:10%;border-style:none;">' + result.get('price') + '</td>'
        text += '<td style="width:10% border-style:none;">'
        text += '<a href="' + result.get('url') + '"title="' + result.get('name') + '"target="_blank">'
        text += '[' + result.get('price') + ']  ' + result.get('name') + '</a>'
        text += '</td>'
        text += '</tr>'

    text += '</table>'
    text += '</p>'
    return_text += text

    return return_text


def search_craigslist(search_name, results_all, results_all_typed):
    #
    # Filter is defined per search request
    #
    search_filter = {
        'searchNearby': search_name.get('searchNearby'),
        'postedToday': search_name.get('postedToday'),
        'srchType': search_name.get('srchType'),
        'hasPic': search_name.get('hasPic'),
        'min_year': search_name.get('min_year'),
        'max_year': search_name.get('max_year'),
        'min_price': search_name.get('min_price'),
        'max_price': search_name.get('max_price')
    }

    try:
        # for each search, iterate each state
        for state in search_name.get('sites'):
            # for each craigslist state, iterate over all the craigslist sites
            for state_sites in list_state_dict:
                # build a search request for the site
                try:
                    for site in state_sites.get(state):
                        clv = CraigslistVehicle(
                            site=site,
                            filters=search_filter
                        )

                        craigslist_results = clv.get_results(sort_by="newest", limit=SEARCH_LIMIT)
                        add_nonduplicate_to_results(craigslist_results, results_all)

                except TypeError:
                    pass

        type_results(results_all, results_all_typed)

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except ConnectionError as e:
        print(e)

    return


def search_autotrader(search_name, results_all, results_all_typed):
    search_filter = {
        'year_from': search_name.get('year_from'),
        'year_to': search_name.get('year_to'),
        'price_from': search_name.get('price_from'),
        'price_to': search_name.get('price_to'),
        'limit': search_name.get('limit'),
        'order': search_name.get('order'),
        'distance': search_name.get('distance')
    }

    try:
        if search_name.get('trucks only') is True:
            html = AUTOTRADER_BASE_TRUCKSONLY_URL + urllib.parse.urlencode(search_filter)
        else:
            html = AUTOTRADER_BASE_URL + urllib.parse.urlencode(search_filter)

        html = urlopen(html)
        bs = BeautifulSoup(html, 'html.parser')
        detail_list = bs.find_all('div', {'class': 'details'})
        counter = 0

        for detail in detail_list:
            counter += 1
            details_html = detail.find('a', {'class': 'name'}, href=True)
            url_link = details_html['href']

            name = detail.find('h3', {'class': 'model'})
            if name.getText() is None:
                continue
            else:
                name = name.getText()

            price = detail.find('h4', {'class': 'price'})
            if price.getText() is None:
                continue
            else:
                price = price.getText()

            for item in results_all:
                if url_link == item.get('url') or name == item.get('name'):
                    break
            else:
                results_all.append(
                    {'id': counter,
                     'name': name,
                     'url': url_link,
                     'price': price})

        type_results(results_all, results_all_typed)

    except AttributeError as e:
        print(e)
    except HTTPError as e:
        print(e.code)
    except URLError as e:
        print(e)


def search_oodle(search_name, results_all, results_all_typed):
    page_listing = [None, 'o=15', 'o=30', 'o=45', 'o=60', 'o=75']
    year_search = '/' + str(search_name['year_from']) + '_' + str(search_name['year_to']) + '-multiple-multiple'
    price_search = '/' + 'price_' + str(search_name['price_from']) + '_' + str(search_name['price_to'])
    order = search_name.get('order')
    distance = search_name.get('distance')
    counter = 0

    html = OODLE_URL_START + year_search + OODLE_URL_END + price_search + '?' + order + '&' + distance
    html = urlopen(html)
    bs = BeautifulSoup(html, 'html.parser')
    pager = bs.find('span', {'id': 'pager'}).getText()
    x = pager_pattern.search(pager)
    total_found = int(pager[x.regs[0][1]:len(pager) - 1])
    total_pages = int(total_found / 15)
    if total_pages >= search_name['pages']:
        total_pages = search_name['pages']

    for i in range(total_pages):

        try:

            html = OODLE_URL_START + year_search + OODLE_URL_END + price_search
            if i == 0:
                html += '?' + order + '&' + distance
            else:
                html += '?' + page_listing[i] + '&' + order + '&' + distance
            # print(html)
            html = urlopen(html)
            bs = BeautifulSoup(html, 'html.parser')

            detail_list = bs.find_all('div', {'class': 'action-wrapper'})
            for detail in detail_list:
                for content in detail.contents:
                    if type(content) == bs4.element.Tag:
                        counter += 1
                        tag = content.contents[3].contents[1]
                        url_link = tag['href']
                        txt = tag.getText()
                        x = oodle_pattern.search(txt)
                        name = txt[0:x.regs[0][0]]
                        price = txt[x.regs[0][1] - 1:]

                        for item in results_all:
                            if url_link == item.get('url') or name == item.get('name'):
                                break
                        else:
                            results_all.append(
                                {'id': counter,
                                 'name': name,
                                 'url': url_link,
                                 'price': price})

        except AttributeError as e:
            print(e)
            return
        except HTTPError as e:
            print(e.code)
            return
        except URLError as e:
            print(e)
            return

    type_results(results_all, results_all_typed)

    return


class Mail:
    def __init__(self, port, smtp_server_domain_name, sender_mail, password):
        self.msg = EmailMessage()
        self.msg['Subject'] = 'Vehicle Reports'
        # self.msg['Bcc'] = ','.join(['spowell@sbcglobal.net'])
        self.msg['Bcc'] = ','.join(['srb42003@yahoo.com', 'rb1327@yahoo.com'])
        self.msg['From'] = 'spowell@powellcattle.com'
        self.port = port
        self.smtp_server_domain_name = smtp_server_domain_name
        self.sender_mail = sender_mail
        self.password = password

    def send(self):
        ssl_context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context) as service:
            service.login(user=self.sender_mail, password=self.password)
            service.send_message(self.msg)
