import os
import shutil
import pandas as pd
import logging

def create_dir(dir: str):
    """Function to create or replace a "tmp" directory"""

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)

def log_records_per(data: pd.DataFrame, group: str):
    '''Function to log the number of records in each group'''

    data['n_records'] = 1

    groups = data.groupby([group]).count().reset_index()

    for i, row in groups.iterrows():

        logging.info("%s_RECORDS=%d" % (row[group], row['n_records']))

def parse_log(line: str):
    '''Function to parse a log line and return a message dict for reporting'''

    line = line.replace('\n','')

    line = line.split(' - ')

    line = {'timestamp': line[0],
            'type': line[1],
            'message': line[2]}

    try:

        kv = line['message'].split('=')

        line['key'] = kv[0]
        line['value'] = kv[1]

    except:

        line['key'] = None
        line['value'] = None

    return(line)
