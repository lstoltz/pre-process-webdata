import pandas as pd
import numpy as np
import os, shutil
class DataFile:
    def __init__(self, csv_file, gps_file, lid_file):
        self.csv_file = csv_file
        self.gps_file = gps_file
        self.lid_file = lid_file

        self.gps_data = []
        self.csv_data = []

        self.in_spike = []
        self.out_spike = []

    def loadGPSData(self):
        with open(self.gps_file[0], 'r') as fp:
            self.gps_data = fp.readlines()
        fp.close()

    def checkGPSData(self):
        stripped_data = []
        if self.hasCoords():
            for item in self.gps_data:
                stripped_data.append(item.strip())
        else:
            pass

        if not stripped_data:
            return False
        else:
            return True # If data good, return true, else false

    def loadCSVData(self):
        self.csv_data = pd.read_csv(self.csv_file)

    def checkCSVData(self):
        if set(['ISO 8601 Time', 'Dissolved Oxygen (mg/l)','Dissolved Oxygen (%)','DO Temperature (C)']).issubset(self.csv_data.columns):
            return True
        else:
            return False

    def tidyGPS(self):
        stripped_data = []
        if self.hasCoords():
            for item in self.gps_data:
                stripped_data.append(item.strip())
        else:
            pass # do nothing
        stripped_data = list(filter(None, stripped_data))
        try:
            for idx, item in  enumerate(stripped_data):
                if (self.hasCoords() and len(stripped_data) == 2):
                    pass
                elif (self.hasCoords() and len(stripped_data) == 1):
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
        filename = self.gps_file[0]
        with open(filename,'w') as fp:
            for item in stripped_data:
                fp.write("%s\n" % item)
            fp.close()

    def hasCoords(self):
        check = []
        for item in self.gps_data:
            check = any(char.isdigit() for char in item)
        return check

    def calcDrops(self):
        idx_a = 0
        idx_b = 1
        in_thresh = 4 # temperature change threshld over one observation for consituting a spike
        out_thresh = -4
        spikes = []
        while idx_b <= self.csv_data.index[-1]:
            spikes.append(self.csv_data.iloc[idx_a, self.csv_data.columns.get_loc('DO Temperature (C)')] - self.csv_data.iloc[idx_b, self.csv_data.columns.get_loc('DO Temperature (C)')])
            idx_a += 1
            idx_b += 1

        for idx in range(0,len(spikes)):
            if spikes[idx] > in_thresh:
                self.in_spike.append(idx+2)

        for idx in range(0, len(spikes)):
            if spikes[idx] < out_thresh:
                self.out_spike.append(idx-2)

    def checkDrops(self):
        temp_thresh = 11
        print(len(self.in_spike))
        print(len(self.out_spike))
        print(self.csv_file)
        if (len(self.in_spike) + len(self.out_spike)) > 3:
            if self.csv_data['DO Temperature (C)'].mean() <= temp_thresh:
                return 2  # add to flagged folder
            else:
                return 0
        elif (len(self.in_spike) + len(self.out_spike)) == 0:
            if self.csv_data['DO Temperature (C)'].mean() <= temp_thresh:
                return 2 # add to flagged folder
            else:
                return 0 # do nothing
        elif (len(self.in_spike) + len(self.out_spike)) == 1 or (len(self.in_spike) + len(self.out_spike)) == 2:
            if self.csv_data['DO Temperature (C)'].mean() <= temp_thresh:
                return 1 # NaN values before in_spike + 2 observations | NaN values after out_spike - 2 observations
            else:
                return 0
    def cleanData(self):
        if len(self.in_spike) == 1 and len(self.out_spike) == 0:
            idx = self.csv_data.loc[0:self.in_spike[0],:]
            self.csv_data.drop(self.csv_data.head(self.in_spike[0]).index, inplace=True)
            self.csv_data.drop(self.csv_data.tail(2).index, inplace=True)

        elif len(self.out_spike) == 1 and len(self.in_spike) == 0:
            self.csv_data.drop(self.csv_data.head(2).index, inplace=True)
            self.csv_data.drop(self.csv_data.tail(self.out_spike).index, inplace=True)

        elif len(self.in_spike) == 1 and len(self.out_spike) ==1:
            self.csv_data.drop(self.csv_data.head(self.in_spike[0]).index, inplace=True)
            self.csv_data.drop(self.csv_data.tail(self.out_spike[0]).index, inplace=True)
             # subset data between the two index values

    def moveComplete(self, DEST):
        output_gps = os.path.join(DEST, os.path.basename(self.gps_file[0]))
        output_lid = os.path.join(DEST, os.path.basename(self.lid_file[0]))
        output_csv = os.path.join(DEST, os.path.basename(self.csv_file))

        shutil.copy(self.gps_file[0], output_gps)
        shutil.copy(self.lid_file[0], output_lid)
        self.csv_data.to_csv(output_csv, index = False, encoding='utf-8-sig', na_rep = 'NaN')

    def moveFlag(self, FLAG):
        output_gps = os.path.join(FLAG, os.path.basename(self.gps_file[0]))
        output_lid = os.path.join(FLAG, os.path.basename(self.lid_file[0]))
        output_csv = os.path.join(FLAG, os.path.basename(self.csv_file))

        shutil.copy(self.gps_file[0], output_gps)
        shutil.copy(self.lid_file[0], output_lid)
        self.csv_data.to_csv(output_csv, index = False, encoding='utf-8-sig', na_rep = 'NaN')
