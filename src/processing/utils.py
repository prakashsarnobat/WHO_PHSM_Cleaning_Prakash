import pandas as pd
import os
import logging
import uuid

def generate_blank_record():
    '''Function to generate a blank record with the correct WHO keys'''

    record = {
        "processed": '',
        "who_id": '',
        "dataset": '',
        "prop_id": '',
        "keep": '',
        "duplicate_record_id": '',
        "who_region": '',
        "country_territory_area": '',
        "iso": '',
        "iso_3166_1_numeric": '',
        "admin_level": '',
        "area_covered": '',
        "prov_category": '',
        "prov_subcategory": '',
        "prov_measure": '',
        "who_code": '',
        "who_category": '',
        "who_subcategory": '',
        "who_measure": '',
        "comments": '',
        "date_start": '',
        "measure_stage": '',
        "prev_measure_number": '',
        "following_measure_number": '',
        "date_end": '',
        "reason_ended": '',
        "targeted": '',
        "enforcement": '',
        "non_compliance_penalty": '',
        "value_usd": '',
        "percent_interest": '',
        "date_entry": '',
        "link": '',
        "link_live": '',
        "link_eng": '',
        "source": '',
        "source_type": '',
        "alt_link": '',
        "alt_link_live": '',
        "alt_link_eng": '',
        "source_alt": '',
        "queries_comments": '',
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

            print(e)

            continue

    return(new_record)


def key_map(new_record: dict, old_record: dict, new_key: str, old_key: str):
    '''Function to move data between records from one key to another'''

    if pd.isnull(old_record[old_key]):

        new_record[new_key] = ''

    else:

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


def assign_who_country_name(record: dict, country_ref: pd.DataFrame, missing_value: str = 'unknown'):
    '''
    Function to assign country names by ISO code

    also adds: who_region, country_territory_area, iso_3166_1_numeric

    '''

    country_ref = country_ref.loc[country_ref['iso'] == record['iso'], :]

    try:

        assert len(country_ref.iloc[:, 1]) == 1

    except Exception as e:

        print(record['iso'])

        record['who_region'] = missing_value
        record['country_territory_area'] = missing_value
        record['iso_3166_1_numeric'] = missing_value

        return(record)

    record['who_region'] = str(country_ref['who_region'].iloc[0])

    record['country_territory_area'] = str(country_ref['country_territory_area'].iloc[0])

    record['iso_3166_1_numeric'] = int(country_ref['iso_3166_1_numeric'].iloc[0])

    return(record)

def assign_who_coding(record: dict, who_coding: pd.DataFrame, missing_value: str = 'unknown'):
    '''
        Function to assign WHO coding to a record

        Test this thoroughly

        Still need to account for possible targeted values

    '''

    prov_measure = who_coding['prov_measure'] == record['prov_measure']
    prov_subcategory = who_coding['prov_subcategory'] == record['prov_subcategory']
    prov_category = who_coding['prov_category'] == record['prov_category']

    coding = who_coding.loc[prov_measure & prov_subcategory & prov_category, :]

    try:

        assert len(coding.iloc[:, 1]) == 1

    except Exception as e:

        # replace this with logging
        # print('Coding values found: ' + str(len(coding.iloc[:, 1])))
        # print('No coding found for dataset: {} prov_measure: {} prov_subcategory: {} prov_category: {}'.format(record['dataset'], record['prov_measure'], record['prov_subcategory'], record['prov_category']))

        record['who_code'] = missing_value
        record['who_measure'] = missing_value
        record['who_subcategory'] = missing_value
        record['who_category'] = missing_value

        return(record)

    record['who_code'] = coding['who_code'].iloc[0]
    record['who_measure'] = coding['who_measure'].iloc[0]
    record['who_subcategory'] = coding['who_subcategory'].iloc[0]
    record['who_category'] = coding['who_category'].iloc[0]

    # try to assign a who_targeted (missing for most records)
    # WARNING: this could overwrite an existing targeted value
    try:

        if coding['who_targeted'].iloc[0] == '':

            raise ValueError

        else:

            record['targeted'] = coding['who_targeted'].iloc[0]

    except Exception as e:

        pass

    # try to assign a non_compliance (missing for most records)
    # WARNING: this could overwrite an existing non_compliance value
    try:

        if coding['non_compliance'].iloc[0] == '':

            raise ValueError

        else:

            record['non_compliance'] = coding['non_compliance'].iloc[0]

    except Exception as e:

        pass

    return(record)
