import json
import sys

try:
    f = open(".\meta-data\sort_filters.json")
    sort_filters_json = json.load(f)
    f.close()
except OSError as e:
    sys.intern(e)


for filters_dict in sort_filters_json['filters']:
    for vehicle in filters_dict:
        print(vehicle)

        for sort_for in filters_dict.get(vehicle):
            print(sort_for)


#         for state_sites in list_state_dict:
#             for site in state_sites.get(state):
#
# for filter_name in sort_filters_json['filters']:
#     print(filter_name.get('name'))
#     final_results = list(dict())
