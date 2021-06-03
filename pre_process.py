import os, shutil
from glob import glob
import pandas as pd
import fnmatch as fn

PATH = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\data"
DEST = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\complete"
FLAG = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\flagged"


def findCSV(PATH):
    csvFiles = [file
                    for path, subdir, files in os.walk(PATH) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.csv'))]
    return csvFiles

def findGPS(PATH):
    gpsFiles = [file
                    for path, subdir, files in os.walk(PATH) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.gps'))]
    return gpsFiles

def findLID(PATH):
    lidFiles = [file
                    for path, subdir, files in os.walk(PATH) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.lid'))]
    return lidFiles

def runChecks():
    for file in findCSV(PATH):
        currentCSV = os.path.basename(file)[:-20]
        gpsFilePath = fn.filter(findGPS(PATH), str('*'+currentCSV+'*'))
        # lidFilePath = fn.filter(findLID(PATH), str('*'+currentCSV+'*'))

        if gpsFilePath == []:
            shutil.copyfile(file, os.path.join(FLAG, os.path.basename(file)))
        # elif lidFilePath == []:
        #     shutil.copyfile(lidFilePath, os.path.join(FLAG, os.path.basename(lidFilePath)))
        else:
            checkLatLon(gpsFilePath)

def checkMissingGPS():
    pass

def checkInWater():
    pass

def checkLatLon(gpsFilePath):
    sws = None
    rws = None

    with open(gpsFilePath[0], 'r') as fp:
        data = fp.readlines()
        fp.close()
    stripped_data = []
    if hasCoords(data):
        for item in data:
            stripped_data.append(item.strip())
    else:
        pass # do nothing
    stripped_data = list(filter(None, stripped_data))
    try:
            for idx, item in  enumerate(stripped_data):
                if (hasCoords(item) and len(stripped_data) == 2):
                    pass
                else:
                    if "RWS" in item:
                        stripped_data[idx] = "RWS: N/A N/A"
                        
                    else:
                        pass
    except:
        pass
    print(data)
    filename = gpsFilePath[0]
    with open(filename,'w') as fp:            
        for item in stripped_data:
            fp.write("%s\n" % item)
        fp.write(data)
        fp.close()
    if not stripped_data:
        return False
    else:
        return True

def hasCoords(inputString):
    check = []
    for item in inputString:
        check = any(char.isdigit() for char in item)
    return check

def main():
    runChecks()

main()