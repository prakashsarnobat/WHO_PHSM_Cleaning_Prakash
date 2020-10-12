"""
process.py
====================================
Functions to combine dataset specific transformers to individual records.

Needed:

individual transformers for each dataset

put shared methods in utils.py

Comprehensive testing

Documentation

Logging

General checks for record numbers etc
"""

from processing import JH_HIT

def process(record: dict):

    if record['dataset'] == 'JH_HIT':

        #apply JH transformer here
        record = JH_HIT.transform(record)

    else:

        raise ValueError('Unknown dataset value.')

    return(record)
