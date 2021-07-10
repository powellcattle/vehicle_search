from craigslist import craigslist
import json

f = open(".\meta-data\craigslist_searches.json")
search_names_json = json.load(f)
f.close()

f = open(".\meta-data\craigsliststates.json")
state_sites = json.load(f)
f.close()

list_state_dict = state_sites['states']

for search_name in search_names_json['allsearches']:
    print(search_name.get('name'))
    final_results = list(dict())

    filters = {
        'searchNearby': search_name.get('searchNearby'),
        'postedToday': search_name.get('postedToday'),
        'srchType': search_name.get('srchType'),
        'hasPic': search_name.get('hasPic'),
        'min_year': search_name.get('min_year'),
        'max_year': search_name.get('max_year')
    }

    for state in search_name.get('sites'):
        print(state)

        for state_sites in list_state_dict:
            for site in state_sites.get(state):
                print(site)

                cl = craigslist.CraigslistForSale(
                    site=site,
                    category='cta',
                    filters=filters
                )

                results = cl.get_results(sort_by="newest", limit=500)
                for result in results:
                    id = result.get('id')
                    name = result.get('name')
                    found = False
                    for row in final_results:
                        if id == row.get('id') or name == row.get('name'):
                            found = True
                            break

                    if not found:
                        final_results.append({'id': result.get('id'), 'name': result.get('name'), 'url': result.get('url'), 'price': result.get('price'), 'where': result.get('where')})
                #

    f = open('C:/Users/spowe/Downloads/'+ search_name.get('name') + '.html', 'w',encoding='utf8')
    text = '<table border="0" style="width: 100%; border-collapse: collapse; border-style: none;">    <thead>    <tr style="text-align: left; border-style: hidden;">        <td style="width: 50%; height: 20px;border-style: hidden;"><strong>Title</strong></td>        <td style="width: 10%; height: 20px;border-style: hidden;"><strong>Price</strong></td>        <td style="width: 20%; height: 20px;border-style: hidden;"><strong>Location</strong></td>    </tr>    </thead>    <tbody>'

    for row in final_results:
        text = text + '<tr style="border-style:none;"><td style="width: 50%;border-style:none;">'
        text += '<a href="' + row.get('url') + '"title="' + row.get('name') + '" target="_blank"><span>' + row.get('name') + '</span></a></td>'
        text += '<td style="width: 10%;border-style: none;">' + row.get('price') + '</td>'
        where = row.get('where')
        if where is None:
            where = ''

        text += '<td style="width: 20%;border-style: none;"><span>' + where + '</span></td></tr>'

    f.write(text)
    f.close()

        # for search in allsearches:
        #     searchname = search.get('name')
        #
        #     cl = craigslist.CraigslistForSale(
        #         site=site,
        #         category='cta',
        #         filters=filters
        #     )
        #
        #     filters = {
        #         'searchNearby': search.get('searchNearby'),
        #         'postedToday': search.get('postedToday'),
        #         'srchType': search.get('srchType'),
        #         'hasPic': search.get('hasPic'),
        #         'min_year': search.get('min_year'),
        #         'max_year': search.get('max_year')
        #     }
        #
        #     for site in search.get('sites'):
        #         cl = craigslist.CraigslistForSale(
        #             site=site,
        #             category='cta',
        #             filters=filters
        #         )
        #

# allsearches = [
#     {
#         'name': 'bobby-generic',
#         'hasPic': 1,
#         'max_year': 1970,
#         'min_year': 1940,
#         'postedToday': 0,
#         'searchNearby': None,
#         'srchType': 'T',
#         'sites': ['flagstaff','phoenix','tucson','reno','lasvegas','lawrence', 'lascruces', 'albuquerque', 'minneapolis', 'desmoines', 'omaha', 'northplatte', 'dallas', 'houston', 'austin', 'sanantonio', 'lafayette', 'neworleans', 'jonesboro', 'littlerock', 'fayar', 'batonrouge']
#     }
# ]
#
# final_results = list(dict())
#
# for search in allsearches:
#     searchname = search.get('name')
#
#     filters = {
#         'searchNearby': search.get('searchNearby'),
#         'postedToday': search.get('postedToday'),
#         'srchType': search.get('srchType'),
#         'hasPic': search.get('hasPic'),
#         'min_year': search.get('min_year'),
#         'max_year': search.get('max_year')
#     }
#
#     for site in search.get('sites'):
#         cl = craigslist.CraigslistForSale(
#             site=site,
#             category='cta',
#             filters=filters
#         )
#
#         results = cl.get_results(sort_by="newest", limit=500)
#         for result in results:
#             id = result.get('id')
#             name = result.get('name')
#             found = False
#             for row in final_results:
#                 if id == row.get('id') or name == row.get('name'):
#                     found = True
#                     break
#
#             if not found:
#                 final_results.append({'id': result.get('id'), 'name': result.get('name'), 'url': result.get('url'), 'price': result.get('price'), 'where': result.get('where')})
#
# f = open('C:/Users/spowe/Downloads/results.html', 'w',encoding='utf8')
#
# text = '<table border="0" style="width: 100%; border-collapse: collapse; border-style: none;">    <thead>    <tr style="text-align: left; border-style: hidden;">        <td style="width: 50%; height: 20px;border-style: hidden;"><strong>Title</strong></td>        <td style="width: 10%; height: 20px;border-style: hidden;"><strong>Price</strong></td>        <td style="width: 20%; height: 20px;border-style: hidden;"><strong>Location</strong></td>    </tr>    </thead>    <tbody>'
#
# for row in final_results:
#     text = text + '<tr style="border-style:none;"><td style="width: 50%;border-style:none;">'
#     text += '<a href="' + row.get('url') + '"title="' + row.get('name') + '" target="_blank"><span>' + row.get('name') + '</span></a></td>'
#     text += '<td style="width: 10%;border-style: none;">' + row.get('price') + '</td>'
#     where = row.get('where')
#     if where is None:
#         where = ''
#
#     text += '<td style="width: 20%;border-style: none;"><span>' + where + '</span></td></tr>'
#
# f.write(text)
# f.close()
