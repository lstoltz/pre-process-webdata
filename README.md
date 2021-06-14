# pre-process-webdata
This script cleans and pre-processes data coming in from 2021 crab pot DO data

To initialize on your setup:

1. retreive appropriate modules
``` python 
pip install -r requirements.txt
```
2. create .env file at the root of project directory with the appropriate data for your setup
``` python
SRC = path_to_dir_where_data_are_stored
DEST = path_to_dir_where_completed_processed_data_are_sent
FLAG = path_to_dir_where_flagged_data_are_sent
LOG = relative_path_to_txt_file
```
The LOG variables stores completed files and checks this file first in order to double process data files. 
## SRC folder
This directory contains raw, unprocessed files that can be retreived from the S3 bucket. The proccessing script is ambiguous to folder structure, therefore all data can just be dumped in this folder and the processor will find and pair up all files. There is logic built into the processors that will filter files that are not suitable for processing. Data included as part of server testing for example will be ignored.

## DEST folder
This directory will contain files that have been cleaned and are immediately ready to be processed onto the website for or data anaylsis. Data are added to this folder if certain conditions have been met regarding the cleaning processes which relies on a combination of average temperature and the number of temperature changes indicative of entering or exiting the water.

## FLAG folder
This directory is home to files that have passed most of the checks for cleaning, but require additional scrutinity to ensure observed valeus are from the water. After running this script, check in the FLAG directory to view files that were not able to automatically be cleaned for soem reason or another. If a file does not pass all checks, the data are not automatically cleaned and it is up to the user to clean the files in the FLAG folder. 
## Using this script
After establishing the appropriate file structure. Data can be continually added to the SRC folder. This folder will grow in length as more data are collected over the course of the summer. This script is designed to allow the user to continually feed data to the SRC folder with the DEST and FLAG folders being populated only with data that have not been run through this script previously. As a result, once files have been processed, the user can delete all files from the DEST and FLAG directories. Take care not to delete the LOG file at the root of of the project, this file stores a list of all previously processed files in said file, and if lost, there will be no record of which files have been processed. 

The GPS file for each file is modified immediately and then saved back into the SRC directory. This step ensures consistancy across all GPS files. Coordinate files that are transmitted from the Deck Data Hub are sporatically inconsistent and therefore it is easier to pre-process all GPS cooridantes reguardless if the data files were collecting data from the ocean or not.


