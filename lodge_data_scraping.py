# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import urllib2
from bs4 import BeautifulSoup
import re

dCustomFoundElevations = {}
dCustomFoundElevations[93] = 767
dCustomFoundElevations[341] = 1030
dCustomFoundElevations[342] = 952
dCustomFoundElevations[343] = 1304
dCustomFoundElevations[438] = 2212

oDataFrame = pd.read_json("lodge-data.json", orient='columns')
oDataFrameJSONColumns = oDataFrame.lodges.apply(pd.Series); # --> parse out json to columns from lodges
iLength = len(oDataFrameJSONColumns['url'])
oDataFrameJSONColumns['meters-above-sea-level'] = pd.Series(np.zeros(iLength), index=oDataFrameJSONColumns.index)

lStrs = ["" for x in range(iLength)]
oDataFrameJSONColumns['latitude'] = pd.Series(lStrs, index=oDataFrameJSONColumns.index)
oDataFrameJSONColumns['longitude'] = pd.Series(lStrs, index=oDataFrameJSONColumns.index)

# Write the raw data into its file
for i, metric in enumerate(metrics):
    with open('data/' + tickers[i] + '.dat', 'w') as fout:
        fout.write(str(metric))
    fout.close()

# loop over all URLs - get info (seehunchen meters)
for index, row in oDataFrameJSONColumns.iterrows():
    page = urllib2.urlopen(row['url']).read()
    soup = BeautifulSoup(page)
    sInfo = str(soup.find("div", {"id": "blockNameAuftrittInner"}))
    sLatitude = str(soup.find("tr", {"id": "huette_geographische_breite"}).find_all("td")[1].p)
    sLatitude = sLatitude.replace("<p>", "").replace("</p>", "")
    sLongitude = str(soup.find("tr", {"id": "huette_geographische_laenge"}).find_all("td")[1].p)
    sLongitude = sLongitude.replace("<p>", "").replace("</p>", "")
    try: 
        re.search(r'Seehöhe (.*?)m', sInfo).group(1) # get the hunchen meters
    except:
        print "That lodge didn't have a meters above sea level listed... trying the custom found elevations..."
        try:
            iElevation = dCustomFoundElevations[index]
        except KeyError:
            print "An elevation wasn't found for " + oDataFrameJSONColumns.at[index, 'name'] 
        else:
            print "Success! Elevation is: " + str(iElevation)
            oDataFrameJSONColumns.at[index, 'meters-above-sea-level'] = iElevation
    else:
        oDataFrameJSONColumns.at[index, 'meters-above-sea-level'] = re.search(r'Seehöhe (.*?)m', sInfo).group(1)
        oDataFrameJSONColumns.at[index, 'latitude'] = sLatitude
        oDataFrameJSONColumns.at[index, 'longitude'] = sLongitude
        
        
    print "Processed " + str(index) + " of " + str(iLength) + " lodges..."

oDataFrameJSONColumns.to_json('lodge-data-extended.json',orient='records')
    