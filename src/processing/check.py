"""
check.py
====================================
Functions to check data attributed inline.
"""

import logging
import pandas as pd


def check_missing_iso(record: dict):
    '''
    Function to check for missing ISO codes

    Note: will not throw an error for "unknown" values which much be
    handled later

    '''

    if pd.isnull(record['iso']):

        raise ValueError('Record: ' + record['who_id'] + ' Dataset: ' + record['dataset'] + ' - Missing ISO code.')

    return(None)


def check_missing_who_code(record: dict):
    '''
    Function to check for null who codes

    Note: will not throw an error for "unknown" values which must be
    handled later

    '''

    if pd.isnull(record['who_code']):

        raise ValueError('Record: ' + record['who_id'] + ' Dataset: ' + record['dataset'] + ' - Missing WHO code.')

    return(None)


def check_record_keys_agree(record: dict, blank_record: dict):

    if record is not None:

        try:

            assert set(blank_record.keys()) == set(record.keys())

        except Exception as e:

            #replace with Logging
            logging.error('Record keys do not agree.')
            logging.error('Keys missing in Record: ' + ', '.join(str(x) for x in set(blank_record.keys()).difference(set(record.keys()))))
            logging.error('Keys present in Record: ' + ', '.join(str(x) for x in set(record.keys()).difference(set(blank_record.keys()))))

            raise e
