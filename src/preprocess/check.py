"""
main.py
====================================
Functions to check input datasets during preprocessing.

test these functions!

"""

import pandas as pd
import logging


def check_input(records: pd.DataFrame, column_config: pd.DataFrame):
    '''Function to unify all input checks'''

    check_column_names(records, column_config)


def check_column_names(records: pd.DataFrame, config: pd.DataFrame):
    '''Function to check that column names agree with config or raise exception'''

    dataset = list(config['dataset'].unique())[0]

    try:

        assert set(records.columns) == set(config['column'])
        logging.info('%s input columns OK.' % dataset)

    except Exception as e:

        message = 'Unexpected %s columns.' % dataset

        logging.error(message)

        raise e
