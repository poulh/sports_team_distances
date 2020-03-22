#!/usr/env python
import pandas as pd
import json
import math

EARTH_RADIUS_MI = 3961
EARTH_RADIUS_KM = 6373

# https://data.healthcare.gov/dataset/Geocodes-USA-with-Counties/52wv-g36k


def distance(radius):
    def dist(lat1, lon1, lat2, lon2):
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d

    return dist


distance_miles = distance(EARTH_RADIUS_MI)
distance_km = distance(EARTH_RADIUS_KM)

teams = pd.read_csv('teams.tsv', sep='\t').set_index('Franchise')

counties = pd.read_csv('county_populations_lat_long.tsv', sep='\t')

distances = pd.DataFrame({
    'County':
    counties['county'].str.replace(' ', '_') + '__' + counties['state']
})

results = pd.DataFrame({
    'County':
    counties['county'].str.replace(' ', '_') + '__' + counties['state']
})
results.set_index('County', inplace=True)

for index, team in teams.iterrows():
    print(team.name)

    distances[team.name] = counties.apply(lambda county: dist(
        county['lat'], county['lon'], team['Latitude'], team['Longitude']),
                                          axis=1)

distances.set_index('County', inplace=True)
results['Closest'] = distances.apply(lambda row: row.idxmin(), axis=1)

#results['Furthest'] = distances.apply(lambda row: row.idxmax(), axis=1)
results.reset_index(inplace=True)

grouped = results.groupby('Closest')['County'].apply(list)

mapdata = {
    "title": "",
    "hidden": [],
    "background": "#ffffff",
    "borders": "#000000"
}

groups = {}

counter = 0
for index, team in teams.iterrows():
    print(team.name)
    try:

        obj = {
            "div": "#box{}".format(counter),
            "label": "",
            "paths": grouped[team.name]
        }
        groups[team['Primary']] = obj
        counter += 1
        print(counter)
    except:
        print("error.")
        pass

mapdata["groups"] = groups

with open('mapdata.json', 'w') as outfile:
    json.dump(mapdata, outfile, indent=2)

#res2.reset_index()
#res2.rename({"1": "Counties"}, axis=1, inplace=True)
# obj = {'groups': {}}

# {
#     "groups": {
#         "#cc3333": {
#             "div": "#box0",
#             "label": "",
#             "paths": ["Pinellas__FL", "Miami-Dade__FL"]
#         },
#         "#74a9cf": {
#             "div": "#box1",
#             "label": "",
#             "paths": ["Crockett__TX", "Shackelford__TX", "Hale__TX"]
#         },
#         "#800026": {
#             "div": "#box2",
#             "label": "",
#             "paths": ["Warren__TN", "Dickson__TN", "Lawrence__TN"]
#         }
#     },
#     "title": "",
#     "hidden": [],
#     "background": "#ffffff",
#     "borders": "#000000"
# }

#print(res2)
#for index, team in teams.iterrows():

# print(results.loc['Pinellas__FL'])
# print(results)
#print(results['Closest'])

# for index, result in results.iterrows():

#     print(result.name)
#     print(type(result.idxmax()))
#     print(result.idxmin())
#     exit()
# print(results.loc['Anchorage__AK'])
# print(results.loc['Anchorage__AK'].idxmax())
#print(distance(27.942, -82.404, 27.888, -82.714))
