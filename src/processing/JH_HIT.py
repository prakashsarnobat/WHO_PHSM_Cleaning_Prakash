"""
JH_HIT.py
====================================
Functions to transform JH_HIT records to WHO format.

Currently removing records with null "locality" and "usa_county" fields
"""
import pandas as pd


def transform(record: dict):

    # generator function of new record with correct keys (shared)

    # replace data in new record with data from old record using column reference (shared)

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
