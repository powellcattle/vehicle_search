import json
import sys

from utils.helper import write_html, search_craigslist, search_autotrader

try:
    f = open("./meta-data/site_searches.json")
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)

if search_names_json is None:
    sys.exit((-1))

results_all = list(dict())
results_all_typed = list(dict())

for search_name in search_names_json['allsearches']:
    name = search_name.get('name')
    search_type = search_name.get('search_site')

    if search_type == 'craigslist':
        search_craigslist(search_name, results_all, results_all_typed)
    elif search_type == 'autotrader':
        search_autotrader(search_name, results_all, results_all_typed)
    else:
        continue

try:
    f = open('C:/dev/reports/test.html', 'w', encoding='utf8')
    text = write_html(results_all_typed, results_all)
    f.write(text)
    f.close()

except OSError as e:
    print(e)
