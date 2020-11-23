import pandas as pd
import re
import os
import logging
import uuid
import random

def generate_blank_record():
    '''Function to generate a blank record with the correct WHO keys'''

    record = {
        "processed": None,
        "uuid": str(uuid.uuid4()),
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
        "original_who_code": None,
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
        "date_processed": None
    }

    return record


def new_id(dataset: str, length: int = 6, existing_ids: list = [None]):
    '''Function to create a unique id given a list of existing ids'''

    id = create_id(dataset, length)

    while id in existing_ids:

        id = create_id(dataset)

    return(id)


def create_id(dataset: str, length: int = 6):
    '''Function to create a random id of characters and numbers'''

    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'

    id = ''

    for i in range(0, length):

        id += random.choice(characters)

    id = dataset + '_' + str(id)

    return id


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
    '''
    Function to move data between records from one key to another

    if a new key is null, data will not be copied. Occurs when some data in a provider dataset is not used in WHO dataset
    '''

    if not pd.isnull(new_key):

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


def get_min_id(fn: str, id_column: str = 'who_id'):
    '''
    Function to open a file and extract the maximum numeric # IDEA:

    This will be the new min id to be incremented.
    '''

    data = pd.read_csv(fn, encoding='latin1', low_memory=False)

    return(max([int(re.findall(r'\d+', x)[0]) for x in data[id_column] if not pd.isna(x)]))


def assign_id(records: dict, min_id: int = 1):
    '''Function to assign a unique ID to each record'''

    #Ensure that no IDs are duplicated by incrementing by 1
    min_id = min_id + 1

    datasets = records['dataset']

    ids = range(min_id, min_id + len(datasets))

    ids = [x + '_' + str(y) for x, y in zip(datasets, ids)]

    records['who_id'] = ids

    return(records)


def assign_who_country_name(record: dict, country_ref: pd.DataFrame, missing_value: str='unknown'):
    '''
    Function to assign country names by ISO code

    also adds: who_region, country_territory_area, iso_3166_1_numeric

    '''

    country_ref = country_ref.loc[country_ref['iso'] == record['iso'], :]

    try:

        assert len(country_ref.iloc[:, 1]) == 1

    except Exception as e:

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

    '''

    prov_measure = who_coding['prov_measure'] == none_to_empty_str(record['prov_measure'])
    prov_subcategory = who_coding['prov_subcategory'] == none_to_empty_str(record['prov_subcategory'])
    prov_category = who_coding['prov_category'] == none_to_empty_str(record['prov_category'])

    coding = who_coding.loc[prov_measure & prov_subcategory & prov_category, :]

    try:

        assert len(coding.iloc[:, 1]) == 1

    except Exception as e:

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

            record['non_compliance_penalty'] = coding['non_compliance'].iloc[0]

    except Exception as e:

        pass

    return(record)


def none_to_empty_str(s):
    '''convert None values to empty strings'''

    if s is None:

        return('')

    else:

        return(s)

def replace_conditional(record: dict, field: str, value: str, replacement: str):
    '''Function to conditionally replace a value in an arbitrary field'''

    if record[field] == value:

        record[field] = replacement

    return(record)


def replace_sensitive_regions(record):
    '''Replace a selection of commonly occuring admin level conflicts'''

    record = shift_sensitive_region(record, 'Kosovo', 'Serbia')
    record = shift_sensitive_region(record, 'Hong Kong', 'China')
    record = shift_sensitive_region(record, 'Taiwan', 'China')
    record = shift_sensitive_region(record, 'Macau', 'China')
    record = shift_sensitive_region(record, 'Macao', 'China')
    record = shift_sensitive_region(record, 'Guadeloupe', 'France')
    record = shift_sensitive_region(record, 'Palestine', 'Israel')

    return(record)


def shift_sensitive_region(record: dict, original_name: str, new_name: str):
    '''Function to demote sensitive country names to area_covered from country_territory_area'''

    if record['country_territory_area'] == original_name:

        record['area_covered'] = record['country_territory_area']

        record['country_territory_area'] = new_name

    return(record)


def add_admin_level(record: dict):
    '''Function to set admin_level values to "national" or "other"'''

    if record['area_covered'] is None:

        record['admin_level'] = 'national'

    else:

        record['admin_level'] = 'other'

    return(record)


def remove_tags(record: dict, keys: list = ['comments']):
    '''Function to remove HTML tags from comments'''

    exp = re.compile(r'<[^>]+>')

    for key in keys:

        try:

            record[key] = exp.sub('', record[key])

        except:

            record[key] = None

    return(record)
