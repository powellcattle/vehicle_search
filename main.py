import json
import sys

from utils.helper import write_html, search_oodle, search_craigslist, search_autotrader

REPORT_DIR = 'C:/dev/reports/'
DATA_DIR = './meta-data/'

search_names_json = dict()
try:
    f = open(DATA_DIR + 'site_searches.json')
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e.strerror)

if search_names_json is None:
    sys.exit((-1))

for search_list in search_names_json:

    name = search_list[0].get("search_name")
    results_all = list(dict())
    results_all_typed = list(dict())

    for idx in range(1, len(search_list)):
        site = search_list[idx][0]
        search_type = site.get("search_site")

        if search_type == 'craigslist':
            # pass
            search_craigslist(site, results_all, results_all_typed)
        elif search_type == 'autotrader':
            # pass
            search_autotrader(site, results_all, results_all_typed)
        elif search_type == 'oodle':
            # pass
            search_oodle(site, results_all, results_all_typed)
        else:
            continue

    try:
        f = open(REPORT_DIR + name + '.html', 'w', encoding='utf8')
        text = write_html(results_all_typed, results_all)
        f.write(text)
        f.close()

    except OSError as e:
        print(e)
