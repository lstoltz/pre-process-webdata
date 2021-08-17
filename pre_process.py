import os, sys
from glob import glob
import fnmatch as fn
from data import DataFile
from dotenv import load_dotenv

load_dotenv()
try:
    parm = sys.argv[1]
    print(parm)
except IndexError:
    print("Error: Please input a regional argument (MA | OR)")
    sys.exit()

SRC = os.getenv("SRC")
DEST = os.getenv("DEST")
FLAG = os.getenv("FLAG")
LOG = os.getenv("LOG")

logger_list = list(range(2002001, 2002040))

def checklog():
    with open(LOG, "r") as fp:
        content = fp.readlines()
    fp.close()
    content = [x.strip() for x in content]
    return content

def findCSV(SRC):
    # find all csv files in the SRC directory
    csvFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.csv'))]
    return csvFiles

def findGPS(SRC):
    # find all gps files in the SRC directory
    gpsFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.gps'))]
    return gpsFiles

def findLID(SRC):
    # find all lid files in the SRC directory
    lidFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.lid'))]
    return lidFiles

def runChecks():
    # main functions that creates the datafile object. 
    for file in findCSV(SRC):
        currentCSV = os.path.basename(file)[:-20]
        try:
            logger_sn = int(currentCSV[:7]) # pulling logger SN off the datafile
        except:
            continue
        if logger_sn not in logger_list and checkArgs() == 1: # checking if the current CSV is acutally an OSU logger
            continue
        elif currentCSV in checklog(): # checking if the current CSV has already been processed
            continue
        else:
            gpsFilePath = fn.filter(findGPS(SRC), str('*'+currentCSV+'*')) # grabbing the lid and gps files that correspond to current csv file
            lidFilePath = fn.filter(findLID(SRC), str('*'+currentCSV+'*'))
        # File load handles checks
            if gpsFilePath and lidFilePath:
                data = DataFile(file, gpsFilePath, lidFilePath, checkArgs()) # putting data into DataFile object
            else:
                continue
            try:
                data.loadGPSData() # reading the GPS data into memory
            except:
                continue

            data.tidyGPS() # reformatting the GPS data, which then saves back to SRC
            gps_good = data.checkGPSData() # returns True or False if the GPS is valid

            if gps_good:
                data.loadCSVData() # loading the CSV data into memory

                if data.checkCSVData(): # makes sure the appropriate headers are in the current CSV
                    data.calcDrops() # conditionally checking the types of temperature changes

                    if data.checkDrops() == 0:
                        continue # do nothing

                    elif data.checkDrops() ==1:
                        data.cleanData() # clean data 
                        data.moveComplete(DEST)
                        data.logFile(LOG) # logs in txt file
                        
                    elif data.checkDrops() == 2:
                        data.moveFlag(FLAG)
                        data.logFile(LOG) # logs in text file
                else:
                    continue
            else:
                continue # GPS data is bad, skipping

def checkArgs():
    try:
        if sys.argv[1] == "OR":
            return 1
        elif sys.argv[1] == "MA":
            return 2
        else:
            print("Error: Input region argument, either MA or OR")
    except IndexError:
        print("Input a region parameter, OR or MA")

def main():
    checklog()
    # print(checkArgs())
    runChecks()


main()
