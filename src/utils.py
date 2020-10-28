import os
import shutil

def create_dir(dir: str):
    """Function to create or replace a "tmp" directory"""

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)

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
