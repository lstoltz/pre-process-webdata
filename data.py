import pandas as pd
import os
import shutil
from glob import glob
import pandas as pd
import fnmatch as fn
import numpy as np
from data.py import DataFile

class DataFile:
    def __init__(self, csv_file, gps_file, lid_file):
        self.csv_file = csv_file
        self.gps_file = gps_file
        self.lid_file = lid_file

        self.gps_data = []
        self.csv_data = [] # pandas file

    ###### Load data ######
    # Loading methods for data files

    def loadGPSData(self):
        with open(self.gps_file[0], 'r') as fp:
            self.gps_data = fp.readlines()

    def loadCSVData(self):
        csv_data = pd.read_csv(self.csv_file)

    def checkGPSData(self):
        # If data good, return true, else false
        return True

    def checkCSVData(self):
        # If data good, return true, else false
        return True

    def tidyGPS(self):
        pass

    def checkLatLon(self):
        pass

    ###### Checks ######
    # Checks/filters for the data sets

    def checkInWater(self):
        # Returns: pos_drop_list, neg_drop_list

        idx_a = 0
        idx_b = 1
        in_thresh = 5
        out_thresh = -5
        spikes = []

        try:
            while idx_b <= len(self.csv_data.index):
                spikes.append(self.csv_data.iloc[idx_a, self.csv_data.columns.get_loc(
                    'DO Temperature (C)')] - self.csv_data.iloc[idx_b, self.csv_data.columns.get_loc('DO Temperature (C)')])
                idx_a += 1
                idx_b += 1
        except:
            pass

        pos_drop = []
        for idx in range(0, len(spikes)):
            if spikes[idx] > in_thresh:
                pos_drop.append(idx)

        neg_drop = []
        for idx in range(0, len(spikes)):
            if spikes[idx] < out_thresh:
                neg_drop.append(idx)

        print(neg_drop)
        return pos_drop, neg_drop

    def checkLatLon(self):
        # with open(gpsFilePath[0], 'r') as fp:
        #     data = fp.readlines()
        #fp.close() # You don't need a close block when using a with statement.
        # As soon as you leave the "with" statement, the file is closed automatically.
        stripped_data = []
        if self.hasCoords(self.gps_data): # TODO Rewrite method call
            for item in self.gps_data:
                stripped_data.append(item.strip())
        else:
            pass

        if not stripped_data:
            return False
        else:
            return True

    # TODO Rewrite this so it uses existing data object, self.gps_data
    def hasCoords(self, inputString):
        check = []
        for item in inputString:
            check = any(char.isdigit() for char in item)
        return check

    def tidyGPS(self):
        # with open(gpsFilePath[0], 'r') as fp:
        #     data = fp.readlines()
        #     fp.close()
        stripped_data = []
        if self.hasCoords(self.gps_data):  # TODO Rewrite hasCoords call, or possibly remove
            for item in self.gps_data:
                stripped_data.append(item.strip())
        else:
            pass  # do nothing
        stripped_data = list(filter(None, stripped_data))
        try:
            for idx, item in enumerate(stripped_data):
                # TODO Rewrite hasCoords call, or possibly remove
                if (self.hasCoords(item) and len(stripped_data) == 2):
                    pass
                # TODO Rewrite hasCoords call, or possibly remove
                elif (self.hasCoords(item) and len(stripped_data) == 1):
                    if "RWS" not in item:
                        stripped_data.insert(0, "RWS: N/A N/A")
                else:
                    if "RWS" in item:
                        stripped_data[idx] = "RWS: N/A N/A"

            if stripped_data == []:
                stripped_data.append("RWS: N/A N/A")
                stripped_data.append("SWS: N/A N/A")

        except:
            pass

        # TODO move this to a separate method. saving should always be a separate operation in case something goes wrong.
        filename = os.path.join(PATH, os.path.basename(self.gps_file[0]))
        with open(filename, 'w') as fp:
            for item in stripped_data:
                fp.write("%s\n" % item)
            fp.close()
