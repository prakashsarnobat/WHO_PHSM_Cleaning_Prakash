"""
main.py
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

import pandas as pd
from processing import JH_HIT, CDC_ITF


def process(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: dict, prov_measure_filter: dict):
    '''Unify individual dataset transformers'''

    if record['dataset'] == 'JH_HIT':

        # apply JH transformer here
        record = JH_HIT.transform(record,
                                  key_ref['JH_HIT'],
                                  country_ref,
                                  who_coding['JH_HIT'],
                                  prov_measure_filter['JH_HIT'])

    elif record['dataset'] == 'CDC_ITF':

        CDC_ITF.transform(record)

    else:

        raise ValueError('Unknown dataset value.')

    return(record)
