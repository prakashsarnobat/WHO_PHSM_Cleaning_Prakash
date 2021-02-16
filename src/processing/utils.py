import pandas as pd
import re
import os
import logging
import uuid
import random


def generate_blank_record():
    """
    Generate a blank record with the correct WHO PHSM keys.

    Other objects requiring the same selection of keys descend from here.

    Returns
    -------
    A blank record with keys in WHO PHSM column format.

    type
        dict.

    """


    record = {
        "processed": None,
        "uuid": str(uuid.uuid4()),
        "who_id": None,
        "who_id_original": None,
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
        "date_processed": None,
        "flag": None,
        "old_targeted": None
    }

    return record


def new_id(dataset: str, length: int = 6, existing_ids: list = [None]):
    """
    Function to create a unique id given a list of existing ids.

    DEPRACATED?

    Parameters
    ----------
    dataset : str
        Dataset to which ids will be added.
    length : int
        Length of new ID number.
    existing_ids : list
        Vector of existing IDs.

    Returns
    -------
    New ID number.
    type
        str.

    """

    id = create_id(dataset, length)

    while id in existing_ids:

        id = create_id(dataset)

    return(id)


def create_id(dataset: str, length: int = 6):
    """
    Create a random id of characters and numbers.

    DEPRACATED?

    Parameters
    ----------
    dataset : str
        Dataset to which ids will be added.
    length : int
        Length of new ID number.

    Returns
    -------
    New ID number.
    type
        str.

    """

    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'

    id = ''

    for i in range(0, length):

        id += random.choice(characters)

    id = dataset + '_' + str(id)

    return id


def apply_key_map(new_record: dict, old_record: dict, key_ref: dict):
    """
    Apply key mapping between two records based on a key reference.

    Example:

    Given `key_ref`: `{'column1':'column2'}`.

    Extracts values from `old_record['column1']` to `new_record['column2']`.

    Parameters
    ----------
    new_record : dict
        Record with WHO PHSM keys.
    old_record : dict
        Record with provider keys.
    key_ref : dict
        Reference for mapping keys between records.

    Returns
    -------
    Record with new values appliued to specified keys.
    type
        dict.

    """

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
    """
    Implements key mapping from `new_record` to `old_record`.

    For more information see `apply_key_map`.

    Parameters
    ----------
    new_record : dict
        Record with WHO PHSM keys.
    old_record : dict
        Record with provider keys.
    new_key : str
        Key in `old_record`.
    old_key : str
        Corresponding key in `new_record`.

    Returns
    -------
    type
        Record with information mapped from `new_key` to `old_key`.

    """

    if not pd.isnull(new_key):

        new_record[new_key] = old_record[old_key]

    return(new_record)


def parse_date(record: dict):
    """Function to parse record date format.

    Currently relying on parsing behaviour of pandas.to_datetime.
    NOTE: This is vulnerable to USA format dates parsed as EU dates

    DEPRACATED?

    Parameters
    ----------
    record : dict
        Dataset record.

    Returns
    -------
    type
        Dataset record.

    """

    record['date_start'] = pd.to_datetime(record['date_start'])
    record['date_end'] = pd.to_datetime(record['date_end'])
    record['date_entry'] = pd.to_datetime(record['date_entry'])

    return(record)


def get_min_id(fn: str, id_column: str = 'who_id'):
    """
    Function to open a file and extract the maximum numeric.

    This will be the new min id to be incremented for the ID field.

    Future: should be replaced by a set difference of existing IDs and an
    arbitrary ID sequence.

    Example:

        Extracts numeric valeu of ID `ACAPS_1234` -> `1234`.

    Parameters
    ----------
    fn : str
        Filename to reference dataset.
    id_column : str
        ID column name in reference dataset.

    Returns
    -------
    Maximum numeric ID value.
    type
        int.

    """

    data = pd.read_csv(fn, encoding='latin1', low_memory=False)

    return(max([int(re.findall(r'\d+', x)[0]) for x in data[id_column] if not pd.isna(x)]))


def assign_id(records: pd.DataFrame, min_id: int = 1):
    """
    Function to assign a unique ID to each record.

    IDs are assigned in the format `DATASET_NUMBER`. i.e. `ACAPS_1234`.

    Parameters
    ----------
    records : pandas.DataFrame
        Dataframe of records which will have ID numbers added.
    min_id : int
        Number to begin incrementing IDs from.

    Returns
    -------
    type
        Dataframe with IDs added.

    """

    #Ensure that no IDs are duplicated by incrementing by 1
    min_id = min_id + 1

    datasets = records['dataset']

    ids = range(min_id, min_id + len(datasets))

    ids = [x + '_' + str(y) for x, y in zip(datasets, ids)]

    records['who_id'] = ids

    return(records)


def assign_who_country_name(record: dict, country_ref: pd.DataFrame, missing_value: str='unknown'):
    """
    Function to assign country names by ISO code.

    Also adds: `who_region`, `country_territory_area`, `iso_3166_1_numeric`.

    WHO recognizes standard country names which are transformed from ISOs defined on provider country names.

    Parameters
    ----------
    record : dict
        Input record.
    country_ref : pd.DataFrame
        Dataframe of country name mappings.
    missing_value : str
        Value to add if name mapping fails - defaults to "unknown".
        This value is recognized by output checks.

    Returns
    -------
    type
        Record with country name mapping applied.

    """

    country_ref = country_ref.loc[country_ref['iso'] == record['iso'], :]

    try:

        assert len(country_ref.iloc[:, 1]) == 1

    except Exception:

        record['who_region'] = missing_value
        record['country_territory_area'] = missing_value
        record['iso_3166_1_numeric'] = missing_value

        return(record)

    record['who_region'] = str(country_ref['who_region'].iloc[0])

    record['country_territory_area'] = str(country_ref['country_territory_area'].iloc[0])

    record['iso_3166_1_numeric'] = int(country_ref['iso_3166_1_numeric'].iloc[0])

    return(record)

def assign_who_coding(record: dict, who_coding: pd.DataFrame, missing_value: str = 'unknown'):
    """
    Assign WHO coding to a record.

    Adds: `who_code`, `who_measure`, `who_subcategory`, `who_category`.

    Optionally adds: `targeted`, `non_compliance`, `enforcement`.

    Transforms provider coding of interventions to WHO PHSM coding.

    Parameters
    ----------
    record : dict
        Input record.
    who_coding : pd.DataFrame
        Dataframe of WHO PHSM intervention mappings.
    missing_value : str
        Value to add if name mapping fails - defaults to "unknown".
        This value is recognized by output checks.

    Returns
    -------
    type
        Record with WHO PHSM code mapping applied.

    """

    prov_measure = who_coding['prov_measure'] == none_to_empty_str(record['prov_measure'])
    prov_subcategory = who_coding['prov_subcategory'] == none_to_empty_str(record['prov_subcategory'])
    prov_category = who_coding['prov_category'] == none_to_empty_str(record['prov_category'])

    coding = who_coding.loc[prov_measure & prov_subcategory & prov_category, :]

    try:

        assert len(coding.iloc[:, 1]) == 1

    except Exception:

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

    except Exception:

        pass

    # try to assign a non_compliance (missing for most records)
    # WARNING: this could overwrite an existing non_compliance value
    try:

        if coding['non_compliance'].iloc[0] == '':

            raise ValueError

        else:

            record['non_compliance_penalty'] = coding['non_compliance'].iloc[0]

    except Exception:

        pass

    # try to assign an enforcement (missing for most records)
    # WARNING: this could overwrite an existing enforcement value
    try:

        if coding['who_enforcement'].iloc[0] == '':

            raise ValueError

        else:

            record['enforcement'] = coding['who_enforcement'].iloc[0]

    except Exception:

        pass

    return(record)


def none_to_empty_str(s):
    """
    Convert None values to an empty string.

    Useful for changing None values for smooth mapping of who coding.

    Parameters
    ----------
    s : type
        String to be converted.

    Returns
    -------
    type
        Outut string, if string equalled None, returns '', else returns original string.

    """

    if s is None:

        return('')

    else:

        return(s)

def replace_conditional(record: dict, field: str, value: str, replacement: str):
    """
    Function to conditionally replace a value in a field.

    Parameters
    ----------
    record : dict
        Input record.
    field : str
        Key of field to be conditionally altered.
    value : str
        Value to identify and replace.
    replacement : str
        Value to insert on replacement.

    Returns
    -------
    type
        Record with specified key altered if `record[key] == value`. Otherwise, the original record is returned.

    """

    if record[field] == value:

        record[field] = replacement

    return(record)


def replace_sensitive_regions(record):
    """
    Replace a selection of commonly occuring admin level issues.

    WHO recognizes certain administrative definitions that differ from ISO conventions.

    Future: Move specific region definitions to `config` directory.

    Parameters
    ----------
    record : type
        Input record.

    Returns
    -------
    type
        Record with sensitive regions changed.

    """

    record = shift_sensitive_region(record, 'Kosovo', 'Serbia')
    record = shift_sensitive_region(record, 'Hong Kong', 'China')
    record = shift_sensitive_region(record, 'Taiwan', 'China')
    record = shift_sensitive_region(record, 'Macau', 'China')
    record = shift_sensitive_region(record, 'Macao', 'China')
    record = shift_sensitive_region(record, 'Guadeloupe', 'France')
    record = shift_sensitive_region(record, 'Palestine', 'Israel')
    record = shift_sensitive_region(record, 'West Bank and Gaza', 'Israel')

    return(record)


def shift_sensitive_region(record: dict, original_name: str, new_name: str):
    """
    Function to demote sensitive country names to `area_covered` from `country_territory_area`.

    Parameters
    ----------
    record : dict
        Input record.
    original_name : str
        Original country name from provider dataset.
    new_name : str
        New WHO-recognised country name.

    Returns
    -------
    type
        Record with sensitive countries changed.

    """

    if record['country_territory_area'] == original_name:

        record['area_covered'] = record['country_territory_area']

        record['country_territory_area'] = new_name

    return(record)


def add_admin_level(record: dict):
    """
    Set admin_level values to "national" or "other".

    If `area_covered` is blank: "national", else: "other".

    Parameters
    ----------
    record : dict
        Input record.

    Returns
    -------
    type
        Record with `admin_level` added.

    """

    if pd.isna(record['admin_level']) and pd.isna(record['area_covered']):

        record['admin_level'] = 'national'

    elif pd.isna(record['admin_level']) and not pd.isna(record['area_covered']):

        record['admin_level'] = 'other'

    return(record)


def remove_tags(record: dict, keys: list = ['comments']):
    """
    Remove HTML tags from defined columns.

    Some datasets (CDC_ITF) provide comments that are enclosed in
    HTML tags for display on the web.

    Identifies content inside of HTML tags and returns content only.

    Example:

    "<p>Content</p>" -> "Content"

    Parameters
    ----------
    record : dict
        Input record.
    keys : list
        List of which keys HTML tage replacement should be applied to.

    Returns
    -------
    type
        Record with HTML tags replaced in the defined tags.

    """

    exp = re.compile(r'<[^>]+>')

    for key in keys:

        try:

            record[key] = exp.sub('', record[key])

        except:

            record[key] = None

    return(record)


def replace_country(record: dict, country_name: str, area_name: str):
    """
    Replace country name with an `area_covered` name.

    Promote a string in `area_covered` to `country_territory_area`.

    Applies to records where a WHO recognised country is defined as an
    administrative region of a different country.

    Parameters
    ----------
    record : dict
        Input record.
    country_name : str
        Country name to be matched.
    area_name : str
        Area name to be matched.

    Returns
    -------
    type
        Record with country `area_covered` promotion applied.

    """

    if record['country_territory_area'] == country_name and record['area_covered'] == area_name:

        record['country_territory_area'] = area_name

        record['area_covered'] = None

    return(record)
