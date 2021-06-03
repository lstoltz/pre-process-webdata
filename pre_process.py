import os, shutil
from glob import glob
import pandas as pd
import fnmatch as fn
import numpy as np
from data.py import DataFile

PATH = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\data"
DEST = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\complete"
FLAG = r"C:\Users\lstol\Documents\Repositories\pre-process-webdata\flagged"

class GoodDataFiles:
    def __init__(self, goodfile) -> None:
        self.keep = []
        self.keep.append(goodfile)

    def showGoodFile(self):
        return self.keep

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
    # Change this to use the for loop to call separate DataFile classes like this
    for file in findCSV(PATH):
        currentCSV = os.path.basename(file)[:-20]
        gpsFilePath = fn.filter(findGPS(PATH), str('*'+currentCSV+'*'))
        lidFilePath = fn.filter(findLID(PATH), str('*'+currentCSV+'*'))

        # File load handles checks
        data = DataFile(file, gpsFilePath, lidFilePath)
        data.loadGPSData(self.gps_file)
        gps_good = data.checkGPSData()

        if (gps_good):
            data.loadCSVData(self.csv_file)
            data.checkCSVData()
        else:
            continue # GPS data is bad, skipping

        # Filtering - add more filters to this as needed
        data.tidyGPS()
        data.checkLatLon()
        data.checkInWater()

        # Copy/store data
        data.store()


    # for file in findCSV(PATH):
    #     currentCSV = os.path.basename(file)[:-20]
    #     gpsFilePath = fn.filter(findGPS(PATH), str('*'+currentCSV+'*'))
    #     # lidFilePath = fn.filter(findLID(PATH), str('*'+currentCSV+'*'))

    #     if gpsFilePath == []:
    #         shutil.copyfile(file, os.path.join(FLAG, os.path.basename(file)))
    #     # elif lidFilePath == []:
    #     #     shutil.copyfile(lidFilePath, os.path.join(FLAG, os.path.basename(lidFilePath)))
    #     else:
    #         tidyGPS(gpsFilePath)
    #         if checkLatLon(gpsFilePath):
    #             checkInWater(file)

def checkInWater(file):
    idx_a = 0
    idx_b = 1
    in_thresh = 5
    out_thresh = -5
    df = pd.read_csv(file)
    spikes = []
    try:
        while idx_b <= len(df.index):
            spikes.append(df.iloc[idx_a, df.columns.get_loc('DO Temperature (C)')] - df.iloc[idx_b, df.columns.get_loc('DO Temperature (C)')])
            idx_a += 1
            idx_b += 1
    except:
        pass
    pos_drop = []
    for idx in range(0,len(spikes)):
        if spikes[idx] > in_thresh:
            pos_drop.append(idx)

    neg_drop = []
    for idx in range(0, len(spikes)):
        if spikes[idx] < out_thresh:
            neg_drop.append(idx)

    print(neg_drop)

def checkLatLon(gpsFilePath):
    with open(gpsFilePath[0], 'r') as fp:
        data = fp.readlines()
    fp.close()
    stripped_data = []
    if hasCoords(data):
        for item in data:
            stripped_data.append(item.strip())
    else:
        pass

    if not stripped_data:
        return False
    else:
        return True

def tidyGPS(gpsFilePath):
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
            elif (hasCoords(item) and len(stripped_data) == 1):
                if "RWS" not in item:
                    stripped_data.insert(0,"RWS: N/A N/A")
            else:
                if "RWS" in item:
                    stripped_data[idx] = "RWS: N/A N/A"

        if stripped_data == []:
            stripped_data.append("RWS: N/A N/A")
            stripped_data.append("SWS: N/A N/A")

    except:
        pass
    filename = os.path.join(PATH, os.path.basename(gpsFilePath[0]))
    with open(filename,'w') as fp:
        for item in stripped_data:
            fp.write("%s\n" % item)
        fp.close()

def hasCoords(inputString):
    check = []
    for item in inputString:
        check = any(char.isdigit() for char in item)
    return check

def main():
    runChecks()

main()
