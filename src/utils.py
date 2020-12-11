import os
import shutil
import pandas as pd
import logging


def create_dir(dir: str):
    """
    Create or replace a "tmp" directory.

    Parameters
    ----------
    dir : str
        Directory name.

    Returns
    -------
    None

    """

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)


def log_records_total(data: pd.DataFrame):
    """
    Log the total number of records in a dataset.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset.

    Returns
    -------
    None

    """

    n_records = len(data.index)

    logging.info("TOTAL_RECORDS=%d" % n_records)


def log_records_per(data: pd.DataFrame, group: str):
    """
    Log the number of records in each group given a grouping column name.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    group : str
        Name of grouping column.

    Returns
    -------
    None

    """

    data = data.copy()

    data['n_records'] = 1

    groups = data.groupby([group]).count().reset_index()

    for i, row in groups.iterrows():

        logging.info("%s_RECORDS=%d" % (row[group], row['n_records']))


def parse_log(line: str):
    """
    Parse a log line and return a message dict for reporting.

    Parameters
    ----------
    line : str
        Line of a log file.

    Returns
    -------
    dict
        Dict containing `timestamp`, `type`, `value` of the log file line.

    """

    line = line.replace('\n', '')

    line = line.split(' - ')

    line = {'timestamp': line[0],
            'type': line[1],
            'message': line[2]}

    try:

        kv = line['message'].split('=')

        line['key'] = kv[0]
        line['value'] = kv[1]

    except Exception:

        line['key'] = None
        line['value'] = None

    return(line)
