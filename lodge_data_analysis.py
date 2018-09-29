import json
import re

with open('lodge-data-extended.json') as json_data:
    dDict = json.load(json_data)
    
def convertToDecimal(sDegrees, sMinutes, sSeconds):
    if sSeconds != "":
        return float(sDegrees) + float(sMinutes) / 60 + float(sSeconds) / 3600
    else:
        return float(sDegrees) + float(sMinutes) / 60
        
def processCoordinate(iIndex, dDict, sType):
    sDegrees = ""
    sMinutes = ""
    sSeconds = ""
    dDict['lodges'][iIndex][sType] = dDict['lodges'][iIndex][sType].replace(",", ".") # european style to US style
    sDegrees = dDict['lodges'][iIndex][sType][:2] # degree value is always the first two letters
    sMinutes = re.search(r'\xb0(.*?)\'', dDict['lodges'][iIndex][sType]).group(1) # decimal value is value between degree and minute sign
    try:
        sSeconds = re.search(r'\'(.*?)\"', dDict['lodges'][iIndex][sType]).group(1) # seconds value
    except:
        sSeconds = ""
    else:
        sSeconds = re.search(r'\'(.*?)\"', dDict['lodges'][iIndex][sType]).group(1) # seconds value
    fDecimalCoordinate = convertToDecimal(sDegrees, sMinutes, sSeconds)
    print fDecimalCoordinate
    dDict['lodges'][iIndex][sType][sType + '-decimal'] = fDecimalCoordinate

for iIndex in range(0, len(dDict['lodges'])):
    processCoordinate(iIndex, dDict, "latitude")
    processCoordinate(iIndex, dDict, "longitude")
    
    