import os, shutil
from glob import glob
import pandas as pd
import fnmatch as fn
import numpy as np
from data import DataFile
from dotenv import load_dotenv

load_dotenv()

SRC = os.getenv("SRC")
DEST = os.getenv("DEST")
FLAG = os.getenv("FLAG")

logger_list = list(range(2002001, 2002040))

def findCSV(SRC):
    csvFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.csv'))]
    return csvFiles

def findGPS(SRC):
    gpsFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.gps'))]
    return gpsFiles

def findLID(SRC):
    lidFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.lid'))]
    return lidFiles

def runChecks():
    # Change this to use the for loop to call separate DataFile classes like this
    for file in findCSV(SRC):
        currentCSV = os.path.basename(file)[:-20]
        try:
            logger_sn = int(currentCSV[:7])
        except:
            continue

        if logger_sn not in logger_list:
            continue
        else:
            gpsFilePath = fn.filter(findGPS(SRC), str('*'+currentCSV+'*'))
            lidFilePath = fn.filter(findLID(SRC), str('*'+currentCSV+'*'))
        # File load handles checks
            if gpsFilePath and lidFilePath:
                data = DataFile(file, gpsFilePath, lidFilePath)
            else:
                continue
            try:
                data.loadGPSData()
            except:
                continue
            data.tidyGPS()
            gps_good = data.checkGPSData()

            if gps_good:
                data.loadCSVData()
                if data.checkCSVData():
                    data.calcDrops()
                    if data.checkDrops() == 0:
                        continue # do nothing
                    elif data.checkDrops() ==1:
                        data.cleanData() # clean data 
                        data.moveComplete(DEST) 
                    elif data.checkDrops() == 2:
                        data.moveFlag(FLAG)
                else:
                    continue
            else:
                continue # GPS data is bad, skipping

def main():
    runChecks()

main()
