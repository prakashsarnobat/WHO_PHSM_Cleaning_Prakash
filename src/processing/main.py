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
from processing import JH_HIT, CDC_ITF, ACAPS, OXCGRT, EURO


def process(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: dict, prov_measure_filter: dict, no_update_phrase: dict):
    """
    Unify individual dataset transformers.

    Applies different transformations for records from different datasets.

    Parameters
    ----------
    record : dict
        Input record.
    key_ref : dict
        Reference for key mapping.
    country_ref : pd.DataFrame
        Reference for WHO accepted country names.
    who_coding : dict
        Reference for WHO coding.
    prov_measure_filter : dict
        Reference for filtering by `prov_measure` values.
    no_update_phrase : dict
        Reference for "no update" phrases.

    Returns
    -------
    type
        Record with transformations applied.

    """

    if record['dataset'] == 'JH_HIT':

        # apply JH transformer here
        record = JH_HIT.transform(record,
                                  key_ref['JH_HIT'],
                                  country_ref,
                                  who_coding['JH_HIT'],
                                  prov_measure_filter['JH_HIT'])

    elif record['dataset'] == 'CDC_ITF':

        record = CDC_ITF.transform(record,
                          key_ref['CDC_ITF'],
                          country_ref,
                          who_coding['CDC_ITF'])

    elif record['dataset'] == 'ACAPS':

        record = ACAPS.transform(record,
                                 key_ref['ACAPS'],
                                 country_ref,
                                 who_coding['ACAPS'])

    elif record['dataset'] == 'OXCGRT':

        record = OXCGRT.transform(record,
                                  key_ref['OXCGRT'],
                                  country_ref,
                                  who_coding['OXCGRT'],
                                  no_update_phrase['OXCGRT'])
                                  
    elif record['dataset'] == 'EURO':

        record = EURO.transform(record,
                                  key_ref['EURO'],
                                  country_ref,
                                  who_coding['EURO'])

    else:

        raise ValueError('Unknown dataset value.')

    return(record)
