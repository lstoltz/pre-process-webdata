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
```
