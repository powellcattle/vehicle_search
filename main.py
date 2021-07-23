import json
import sys

from utils.helper import write_html, search_craigslist, search_autotrader

search_names_json = dict()
try:
    f = open("./meta-data/site_searches.json")
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e.strerror)

# for search_list in search_names_json:
#     search_name = search_list[0].get("search_name")
#     for i in range(1, len(search_list)):
#         site_site = search_list[i][0]
#         site_site.get("search_site")
#         pass

if search_names_json is None:
    sys.exit((-1))

results_all = list(dict())
results_all_typed = list(dict())

for search_list in search_names_json:
    name = search_list[0].get("search_name")
    for i in range(1, len(search_list)):
        site = search_list[i][0]
        search_type = site.get("search_site")

        if search_type == 'craigslist':
            search_craigslist(site, results_all, results_all_typed)
        elif search_type == 'autotrader':
            search_autotrader(site, results_all, results_all_typed)
        else:
            continue

    try:
        f = open('C:/dev/reports/' + name + '.html', 'w', encoding='utf8')
        text = write_html(results_all_typed, results_all)
        f.write(text)
        f.close()

    except OSError as e:
        print(e)
