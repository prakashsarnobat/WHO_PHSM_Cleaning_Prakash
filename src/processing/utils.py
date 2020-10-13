import pandas as pd
import os
import logging
import uuid

def generate_blank_record():
    '''Function to generate a blank record with the correct WHO keys'''

    record = {
        "processed": None,
        "who_id": None,
        "dataset": None,
        "prop_id": None,
        "keep": None,
        "duplicate_record_id": None,
        "who_region": None,
        "country_territory_area": None,
        "iso": None,
        "iso_3166_1_numeric": None,
        "admin_level": None,
        "area_covered": None,
        "prov_category": None,
        "prov_subcategory": None,
        "prov_measure": None,
        "who_code": None,
        "who_category": None,
        "who_subcategory": None,
        "who_measure": None,
        "comments": None,
        "date_start": None,
        "measure_stage": None,
        "prev_measure_number": None,
        "following_measure_number": None,
        "date_end": None,
        "reason_ended": None,
        "targeted": None,
        "enforcement": None,
        "non_compliance_penalty": None,
        "value_usd": None,
        "percent_interest": None,
        "date_entry": None,
        "link": None,
        "link_live": None,
        "link_eng": None,
        "source": None,
        "source_type": None,
        "alt_link": None,
        "alt_link_live": None,
        "alt_link_eng": None,
        "source_alt": None,
        "queries_comments": None,
    }

    return record


def apply_key_map(new_record: dict, old_record: dict, key_ref: dict):
    '''Function to apply key mapping between two records based on a key reference'''

    for key in key_ref:

        try:
            new_record = key_map(new_record,
                                 old_record,
                                 key['new_key'],
                                 key['old_key'])

        except Exception as e:

            continue

    return(new_record)


def key_map(new_record: dict, old_record: dict, new_key: str, old_key: str):
    '''Function to move data between records from one key to another'''

    new_record[new_key] = old_record[old_key]

    return(new_record)


def parse_date(record: dict):
    '''
        Function to parse record date format

        Currently relying on parsing behaviour of pandas.to_datetime.
        NOTE: This is vulnerable to USA format dates parsed as EU dates

    '''

    record['date_start'] = pd.to_datetime(record['date_start'])
    record['date_end'] = pd.to_datetime(record['date_end'])
    record['date_entry'] = pd.to_datetime(record['date_entry'])

    return(record)


def assign_id(record):
    '''Function to assign a unique ID to each record'''

    record['who_id'] = str(uuid.uuid4())

    return(record)


def assign_who_country_name(record: dict, country_ref: pd.DataFrame):
    '''
    Function to assign country names by ISO code

    also adds: who_region, country_territory_area, iso_3166_1_numeric

    '''

    country_ref = country_ref.loc[country_ref['iso'] == record['iso'], :]

    record['who_region'] = str(country_ref['who_region'].iloc[0])

    record['country_territory_area'] = str(country_ref['country_territory_area'].iloc[0])

    record['iso_3166_1_numeric'] = int(country_ref['iso_3166_1_numeric'].iloc[0])

    return(record)
