import json
import sys
from urllib.error import HTTPError
from urllib.error import URLError

from utils.helper import add_nonduplicate_to_results, type_results, write_html
from utils.vehicle import CraigslistVehicle

try:
    f = open("./meta-data/craigslist_searches.json")
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

try:
    f = open("./meta-data/sort_filters.json")
    sort_filters_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

stateSites = []
try:
    f = open("./meta-data/site_searches.json")
    searches_json = json.load(f)

    stateSites = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

list_state_dict = stateSites['states']
SEARCH_LIMIT = 100

if search_names_json is None:
    sys.exit((-1))

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

# Append Class Auto Trader to CraigsList

    try:

        f = open('C:/dev/reports/' + search_name.get('name') + '.html', 'w', encoding='utf8')
        text = write_html(results_all_typed, results_all)
        f.write(text)
        f.close()

    except OSError as e:
        print(e)
