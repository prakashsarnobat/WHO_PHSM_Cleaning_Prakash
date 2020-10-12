"""
JH_HIT.py
====================================
Functions to transform JH_HIT records to WHO format.

Currently removing records with null "locality" and "usa_county" fields
"""
import pandas as pd
from processing import utils

def transform(record: dict):

    # generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # replace data in new record with data from old record using column
    # reference (shared)
    key_ref = pd.read_csv('config/key_map/JH_HIT.csv')
    key_ref = key_ref.to_dict(orient='records')

    new_record = utils.apply_key_map(new_record, record, key_ref)

    # Handle date - infer format (shared)

    # Assign unique ID (shared)

    # replace non ascii characters (shared)

    # check for missing ISO codes (shared)

    # Join WHO accepted country names (shared)

    # Join who coding from lookup (shared)

    # check for missing WHO codes (shared)

    #custom JH things here

    # Currently removing records with null "locality" and "usa_county" fields
    #if pd.isnull(record['locality']) and pd.isnull(record['usa_county']):
    #    return(None)

    return(record)
