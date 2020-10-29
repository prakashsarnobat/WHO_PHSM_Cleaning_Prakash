"""
main.py
====================================
Functions to check input datasets during preprocessing.

test these functions!

"""

import pandas as pd
import logging
from datetime import datetime


def check_input(records: pd.DataFrame, column_config: pd.DataFrame):
    '''Function to unify all input checks'''

    check_column_names(records, column_config)


def check_column_names(records: pd.DataFrame, config: pd.DataFrame, log: bool = True):
    '''Function to check that column names agree with config or raise exception'''

    dataset = list(config['dataset'].unique())[0]

    try:

        assert set(records.columns) == set(config['column'])

        if log:

            logging.info('INPUT_CHECK_SUCCESS=%s input columns OK.' % dataset)

    except Exception as e:

        message = 'INPUT_CHECK_SUCCESS=Unexpected %s columns.' % dataset

        if log:

            logging.error(message)

        raise e

def check_date_format(data: pd.DataFrame, config: pd.DataFrame, dataset: str, log: bool = True):
    '''Function to check that an input date is in the expected format'''

    format = config.loc[config['dataset'] == dataset, 'format'].item()
    date_column = config.loc[config['dataset'] == dataset, 'date_column'].item()

    res = [validate_date_format(x, format) for x in data[date_column] if x is None]

    try:

        assert len(res) == 0

        if log:

            logging.info('INPUT_CHECK_SUCCESS=%s %s date format is %s OK.' % (dataset, date_column, format))

    except:

        if log:

            logging.info('INPUT_CHECK_FAILURE=%s %s %d dates not in the format %s.' % (dataset, date_column, len(res), format))

def validate_date_format(date, format):
    '''Function to return None if a date format does not parse'''

    try:

        return(datetime.strptime(date, format))

    except:

        return(None)
