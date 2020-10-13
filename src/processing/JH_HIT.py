"""
JH_HIT.py
====================================
Functions to transform JH_HIT records to WHO format.
"""
import pandas as pd
from processing import utils
from processing import check

def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame):

    # generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # replace data in new record with data from old record using column
    # reference (shared)
    record = utils.apply_key_map(new_record, record, key_ref)

    # Handle date - infer format (shared)
    record = utils.parse_date(record)

    # Assign unique ID (shared)
    record = utils.assign_id(record)

    # replace non ascii characters (shared)

    # check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # Join WHO accepted country names (shared)
    utils.assign_who_country_name(record, country_ref)

    # Join who coding from lookup (shared)

    # check for missing WHO codes (shared)

    #custom JH things here

    # Currently removing records with null "locality" and "usa_county" fields
    #if pd.isnull(record['locality']) and pd.isnull(record['usa_county']):
    #    return(None)

    return(record)
