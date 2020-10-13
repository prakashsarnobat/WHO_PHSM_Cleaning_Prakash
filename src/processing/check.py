"""
check.py
====================================
Functions to check data attributed inline.
"""

import logging
import pandas as pd

def check_missing_iso(record):

     if pd.isnull(record['iso']):

         raise ValueError('Record: ' + record['who_id'] + ' Dataset: ' + record['dataset'] + ' - Missing ISO code.')

     return(None)
