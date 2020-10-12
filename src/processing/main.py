"""
process.py
====================================
Functions to combine dataset specific transformers to individual records.
"""

from processing import JH_HIT


def process(record: dict):

    if record['dataset'] == 'JH_HIT':

        #apply JH transformer here
        record = JH_HIT.transform(record)

    else:

        raise ValueError('Unknown dataset value.')

    return(record)
