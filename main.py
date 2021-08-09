import json
import mimetypes
import os
import sys

from utils.helper import write_html, search_oodle, search_craigslist, search_autotrader, ReportMailer, \
    search_classiccars, configure_logger

REPORT_DIR = '../../dev/reports/'
DATA_DIR = './meta-data/'

_logger = None
# need to remove all .html files from REPORT DIR before starting
if __name__ == '__main__':
    _logger = configure_logger('vehicle_search', '../reports/vehicle_search.log')

# read external search criteria
search_names_json = None
try:
    file_path = open(DATA_DIR + 'site_searches.json')
    search_names_json = json.load(file_path)
    file_path.close()
except OSError as e:
    _logger.error('Problem opening site_searches.json: %s', e.strerror)
    sys.exit(-1)
except Exception as e:
    _logger.error('Unknown Error %s', e)
    sys.exit(-1)

# each search name can have ..n searches on various search sites
for search_list in search_names_json:

    name = search_list[0].get("search_name")
    _logger.info('Loading ' + name + ' search')
    results_all = list(dict())
    results_all_typed = list(dict())

    for idx in range(1, len(search_list)):
        site = search_list[idx][0]
        # represents the site e.g., craigslist or autotrader...
        search_type = site.get("search_site")
        _logger.info('Searching ' + search_type)
        if search_type == 'craigslist':
            # pass
            search_craigslist(site, results_all, results_all_typed)
        elif search_type == 'autotrader':
            # pass
            search_autotrader(site, results_all, results_all_typed)
        elif search_type == 'oodle':
            # pass
            search_oodle(site, results_all, results_all_typed)
        elif search_type == 'classiccars':
            # pass
            search_classiccars(site, results_all, results_all_typed)
        else:
            continue

    try:
        # after all the criteria is completed for a site name, write the results to HTML
        file_name = os.path.join(REPORT_DIR, (name + '.html'))
        _logger.debug(file_name)
        file_path = open(file_name, 'w', encoding='utf8')
        text = write_html(results_all_typed, results_all)
        file_path.write(text)
        file_path.close()
    except OSError as e:
        _logger.error('Problem writing HTML reports %s', e.strerror)
        sys.exit(-1)
    except Exception as e:
        _logger.error('Unknown Error %s', e)
        sys.exit(-1)

# read smtp email server information to send reports
mail = None
try:
    file_path = open(DATA_DIR + 'email_server.json')
    es = json.load(file_path)
    mail = ReportMailer(port=es['port'],
                        smtp_server_domain_name=es['smtp_server_domain_name'],
                        sender_mail=es['sender_mail'],
                        password=es['password'])
    file_path.close()

    for filename in os.listdir(REPORT_DIR):
        mime_type = mimetypes.guess_type(filename)
        mime_type, mime_subtype = mime_type[0].split('/', 1)
        if mime_type != 'text' or mime_subtype != 'html':
            continue

        file_path = os.path.join(REPORT_DIR, filename)
        with open(file_path, 'rb') as attachment:
            mail.msg.add_attachment(attachment.read(), maintype=mime_type, subtype=mime_subtype, filename=filename)

    mail.send()
    _logger.info('Email sent')

except OSError as e:
    _logger.error('Problem with emailing reports %s', e.strerror)
    sys.exit(-1)

except Exception as e:
    _logger.error('Unknown Error %s', e)
    sys.exit(-1)
