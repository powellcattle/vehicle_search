import sys

from craigslist import craigslist

import json

from vehicle import CraigslistVehicle

try:
    f = open(".\meta-data\craigslist_searches.json")
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

try:
    f = open(".\meta-data\sort_filters.json")
    sort_filters_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

try:
    f = open(".\meta-data\craigsliststates.json")
    state_sites = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

list_state_dict = state_sites['states']


def write_html(results_all_typed, results_all):
    return_text = ''

    for filters_dict in sort_filters_json['filters']:

        for vehicle in filters_dict:
            text = '<table border="0" style="width: 100%; border-collapse: collapse; border-style: none;"><thead>' \
                   '<tr style="text-align: left; border-style: hidden;"><td style="width: 50%;' \
                   ' height: 20px;border-style: hidden;"><strong>' + vehicle.upper() + '</strong></td>' \
                    '<td style="width: 10%;height: 20px;border-style: hidden;"><strong>Price</strong></td>' \
                    '<td style="width: 20%;height: 20px;border-style: hidden;"><strong>Location</strong>' \
                    '</td></tr></thead><tbody>'

            for result in results_all_typed:
                if result.get('vtype') == vehicle:
                    text += '<tr style="border-style:none;">'
                    text += '<td style="width:50%;border-style:none;">'
                    text += '<a href="' + result.get('url') + '"title="' + result.get('name') + '"target="_blank">'
                    text += '<span>' + result.get('name') + '</span>'
                    text += '</a>'
                    text += '</td>'
                    text += '<td style="width:10%;border-style:none;"><span>' + result.get('price') + '</span></td>'
                    where = result.get('where')
                    if where is None:
                        where = ''
                    text += '<td style="width: 20%;border-style: none;"><span>' + where + '</span></td>'
                    text += '</tr>'
        return_text += text

    text = '<table border="0" style="width: 100%; border-collapse: collapse; border-style: none;">    <thead>    ' \
           '<tr style="text-align: left; border-style: hidden;"><td style="width: 50%;' \
           ' height: 20px;border-style: hidden;"><strong> ALL VEHICLES</strong></td>' \
           '<td style="width: 10%;' \
           ' height: 20px;border-style: hidden;"><strong>Price</strong></td> <td style="width: 20%;' \
           ' height: 20px;border-style: hidden;"><strong>Location</strong></td></tr> </thead><tbody>'

    for result in results_all:
        text += '<tr style="border-style:none;">'
        text += '<td style="width: 50%;border-style:none;">'
        text += '<a href="' + result.get('url') + '"title="' + result.get('name') + '"target="_blank">'
        text += '<span>' + result.get('name') + '</span>'
        text += '</a>'
        text += '</td>'
        text += '<td style="width: 10%;border-style: none;">' + result.get('price') + '</td>'
        where = result.get('where')
        if where is None:
            where = ''
        text += '<td style="width: 20%;border-style: none;"><span>' + where + '</span></td></tr>'

    return_text += text

    return (return_text)


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
                 'price': result.get('price'), 'where': result.get('where')})

    return add_to


def type_results(results_all, results_all_typed):
    for result in results_all:
        for filters_dict in sort_filters_json['filters']:
            for vehicle in filters_dict:
                for sort_for in filters_dict.get(vehicle):
                    name = result.get('name').lower()
                    if name.__contains__(sort_for):
                        results_all_typed.append(
                            {'vtype': vehicle, 'id': result.get('id'),
                             'name': result.get('name'),
                             'url': result.get('url'),
                             'price': result.get('price'),
                             'where': result.get('where')})
                        break


for search_name in search_names_json['allsearches']:

    results_all = list(dict())
    results_all_typed = list(dict())
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

                    craigslist_results = cl.get_results(sort_by="newest", limit=50)
                    add_nonduplicate_to_results(craigslist_results, results_all)
            except TypeError:
                pass

    type_results(results_all, results_all_typed)

    f = open('C:/dev/reports/' + search_name.get('name') + '.html', 'w', encoding='utf8')
    text = write_html(results_all_typed, results_all)
    f.write(text)
    f.close()
