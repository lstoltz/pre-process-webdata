import os
from glob import glob
from dotenv import load_dotenv

load_dotenv()
SRC = os.getenv("SRC")

def findCSV(SRC):
    # find all csv files in the SRC directory
    csvFiles = [file
                    for path, subdir, files in os.walk(SRC) # find all csv files in a directory
                    for file in glob(os.path.join(path, '*.csv'))]
    return csvFiles

all_files = findCSV(SRC)
current_year_files = []
for file in all_files:
    if "202205" in file:
        current_year_files.append(file)

print(len(current_year_files))