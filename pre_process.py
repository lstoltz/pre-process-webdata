import os, shutil
from glob import glob
import pandas as pd
import fnmatch as fn
import numpy as np
from data import DataFile
from dotenv import load_dotenv

load_dotenv()

PATH = os.getenv("PATH")
DEST = os.getenv("DEST")
FLAG = os.getenv("FLAG")

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
        try:
            data.loadGPSData()
        except:
            continue
        data.tidyGPS()
        gps_good = data.checkGPSData()

        if gps_good:
            data.loadCSVData()
            if data.checkCSVData():
                if data.checkDrops() == 0:
                    continue # do nothing
                elif data.checkDrops() ==1:
                    data.cleanData() # clean data
                    
                elif data.checkDrops() == 2:
                    pass # add to flagged folder
            else:
                continue
        else:
            continue # GPS data is bad, skipping

def main():
    runChecks()

main()
