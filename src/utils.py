import os
import shutil
import pandas as pd

def create_dir(dir: str):
    """Function to create or replace a "tmp" directory"""

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)

def log_records_per(data: pd.DataFrame, group: str):
    '''Function to log the number of records in each group'''

    groups = data.groupby([group]).count()

    count_col = groups.columns[1]

    for i, row in groups.iterrows():

        logging.info("%s_RECORDS=%d" % (row.index, row[count_col]))

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
