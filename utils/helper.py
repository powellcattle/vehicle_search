import re
import json
import sys
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from utils.vehicle import CraigslistVehicle

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

list_state_dict = stateSites['states']
SEARCH_LIMIT = 100


def find_whole_word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def add_nonduplicate_to_results(results, final_results):
    add_to = True

    for result in results:
        id = result.get('id')
        name = result.get('name')

        for row in final_results:
            if id == row.get('id') or name == row.get('name'):
                add_to = False
                break

        if add_to:
            final_results.append(
                {'id': result.get('id'), 'name': result.get('name'),
                 'url': result.get('url'),
                 'price': result.get('price')})

    return add_to


def type_results(results_all, results_all_typed):
    for result in results_all:
        for filters_dict in sort_filters_json['filters']:
            for vehicle in filters_dict:
                for sort_for in filters_dict.get(vehicle):
                    name = result.get('name').lower()
                    if find_whole_word(sort_for)(name):
                        results_all_typed.append(
                            {'vtype': vehicle, 'id': result.get('id'),
                             'name': result.get('name'),
                             'url': result.get('url'),
                             'price': result.get('price')})
                        break


def write_html(results_all_typed, results_all):
    return_text = ''

    for filters_dict in sort_filters_json['filters']:

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
    added_to = True
    #
    # Filter is defined per search request
    #
    search_filter = {
        'searchNearby': search_name.get('searchNearby'),
        'postedToday': search_name.get('postedToday'),
        'srchType': search_name.get('srchType'),
        'hasPic': search_name.get('hasPic'),
        'min_year': search_name.get('min_year'),
        'max_year': search_name.get('max_year')
    }

    # for each search, iterate each state
    try:
        for state in search_name.get('sites'):
            # for each craigslist state, iterate over all sites
            for state_sites in list_state_dict:
                # iterate over each state site
                try:
                    for site in state_sites.get(state):
                        cl = CraigslistVehicle(
                            site=site,
                            filters=search_filter
                        )

                        craigslist_results = cl.get_results(sort_by="newest", limit=SEARCH_LIMIT)
                        add_nonduplicate_to_results(craigslist_results, results_all)

                except TypeError:
                    pass

        type_results(results_all, results_all_typed)

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)

    return


def search_autotrader(search_name, results_all, results_all_typed):
    html = urlopen('https://classics.autotrader.com/classic-cars-for-sale/classic_trucks-for-sale?year_from=1940&year_to=1970&price_to=20000&seller_type=seller&limit=500&order=created+desc&distance=nationwide')

    try:
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

            results_all.append(
                {'id': counter,
                 'name': name,
                 'url': url_link,
                 'price': price})

        type_results(results_all, results_all_typed)

    except AttributeError as e:
        print(e)
        sys.exit(-1)
