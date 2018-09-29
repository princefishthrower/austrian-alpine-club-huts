from bs4 import BeautifulSoup
from unidecode import unidecode
import json
oJSON = {}

lines = [line.rstrip('\n') for line in open('raw-lodge-data.html')]

sRootUrl = "https://www.alpenverein.at" # /huetten/index.php?huette_nr=1638

lDictList = []
for line in lines:
    soup = BeautifulSoup(line, 'html.parser')
    rows = soup.find("table", {"id": "tableList"}).find("tbody").find_all("tr")
    iIndex = 0
    for row in rows:
        dData = {}
        sInfo = str(row.find_all("td")[1].div.br)
        sInfo = sInfo.replace("</br>", "")
        lInfo = sInfo.split("<br>")
        sName = str(row.find_all("td")[1].div.b)
        sName = sName.replace("<b>", "").replace("</b>","")
        sState = lInfo[1]
        sMountainGroup = lInfo[2]
        sMountainGroup = sMountainGroup.replace("(", "").replace(")", "")
        sUrl = sRootUrl + row.find_all("a")[0]['href']
        dData["name"] = sName
        dData["state"] = sState
        dData["mountain-group"] = sMountainGroup
        dData["url"] = sUrl
        lDictList.append(dData)
        iIndex = iIndex + 1
        
oJSON['lodges'] = lDictList
with open('lodge-data.json', 'w') as outfile:
    json.dump(oJSON, outfile)