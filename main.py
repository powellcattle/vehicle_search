import json
import mimetypes
import os
import sys

from myemail import Mail
from utils.helper import write_html, search_oodle, search_craigslist, search_autotrader

REPORT_DIR = '../../dev/reports/'
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

# read smtp email server information to send reports
mail = None
try:
    f = open(DATA_DIR + 'email_server.json')
    es = json.load(f)
    mail = Mail(port=es['port'],
                smtp_server_domain_name=es['smtp_server_domain_name'],
                sender_mail=es['sender_mail'],
                password=es['password'])
    f.close()

    for filename in os.listdir(REPORT_DIR):
        mime_type = mimetypes.guess_type(filename)
        mime_type, mime_subtype = mime_type[0].split('/', 1)
        f = os.path.join(REPORT_DIR, filename)

        with open(f, 'rb') as ap:
            mail.msg.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=f)

    mail.send()

except OSError as e:
    sys.intern(e.strerror)
