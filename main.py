import json
import logging
import mimetypes
import os
import sys

from utils.helper import write_html, search_oodle, search_craigslist, search_autotrader, ReportMailer


def _init_logger():
    logger = logging.getLogger('vehicle_search')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s: %(levelname)s: %(name)s: %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


_logger = None
# need to remove all .html files from REPORT DIR before starting
if __name__ == '__main__':
    _init_logger()
    _logger = logging.getLogger('vehicle_search')

REPORT_DIR = '../../dev/reports/'
DATA_DIR = './meta-data/'

# read external search criteria
search_names_json = None
try:
    f = open(DATA_DIR + 'site_searches.json')
    search_names_json = json.load(f)
    f.close()
except OSError as e:
    _logger.error('Problem opening site_searches.json: %s', e.strerror)
    sys.exit(-1)
except:
    _logger.error('Unknown Error %s', sys.exc_info()[2])
    sys.exit(-1)

# each search name can have ..n searches on various search sites
for search_list in search_names_json:

    name = search_list[0].get("search_name")
    results_all = list(dict())
    results_all_typed = list(dict())

    for idx in range(1, len(search_list)):
        site = search_list[idx][0]
        # represents the site e.g., craigslist or autotrader...
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
        # after all the criteria is completed for a site name, write the results to HTML
        f = open(REPORT_DIR + name + '.html', 'w', encoding='utf8')
        text = write_html(results_all_typed, results_all)
        f.write(text)
        f.close()
    except OSError as e:
        _logger.error('Problem writing HTML reports %s', e.strerror)
        sys.exit(-1)
    except:
        _logger.error('Unknown Error %s', sys.exc_info()[2])
        sys.exit(-1)

# read smtp email server information to send reports
mail = None
try:
    f = open(DATA_DIR + 'email_server.json')
    es = json.load(f)
    mail = ReportMailer(port=es['port'],
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
    _logger.error('Problem with emailing reports %s', e.strerror)
    sys.exit(-1)

except:
    _logger.error('Unknown Error %s', sys.exc_info()[2])
    sys.exit(-1)
