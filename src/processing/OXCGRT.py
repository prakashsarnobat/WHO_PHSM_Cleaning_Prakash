"""
OXCGRT.py
====================================
Transform OXCGRT records to WHO PHSM format.

**Data Source:**
`https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv <https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv>`_

**Processing Steps:**
1. generator function of new record with correct keys (shared)
2. replace data in new record with data from old record using column reference (shared)
3. Assign unique ID (shared)
4. Handle date formatting

"""

import pandas as pd
from countrycode.countrycode import countrycode
import re

# hot fix for sys.path issues in test environment
try:

    from processing import utils
    from processing import check

except Exception as e:

    from src.processing import utils
    from src.processing import check


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame, no_update_phrase: pd.DataFrame):

    # 1. generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # 2. replace data in new record with data from old record using column
    # reference (shared)
    record = utils.apply_key_map(new_record, record, key_ref)

    # 3. Assign unique ID (shared)
    #record = utils.assign_id(record)

    # 4. Handle date formatting
    record = utils.parse_date(record)

    # 8. replace sensitive country names
    record = utils.replace_sensitive_regions(record)

    # 7. Make manual country name changes
    record = utils.replace_conditional(record, 'country_territory_area', 'Eswatini', 'Swaziland')
    record = utils.replace_conditional(record, 'country_territory_area', 'South Korea', 'Korea')

    # 9. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 10. check missing ISO
    check.check_missing_iso(record)

    # Remove records where there is no data in prov_subcategory
    if record['prov_subcategory'] == 0:

        return(None)

    # Removes information in flag variables for now
    record['prov_measure'] = 0
    record['prov_subcategory'] = int(record['prov_subcategory'])
    record['prov_measure'] = int(record['prov_measure'])

    # 11. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    record = financial_measures(record)

    # 12. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 13. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 16. Add WHO PHSM admin_level values
    record = utils.add_admin_level(record)

    record = utils.remove_tags(record)

    # 17. Remove update records
    record = assign_comment_links(record)

    # Filter out records with "no update" phrases
    record = label_update_phrase(record, list(no_update_phrase['phrase']))

    return(record)


def label_update_phrase(record: dict, phrases: list):
    '''
    Function to assign who_code == 10 and 'Not of interest'
    to records with no update phrases
    '''

    if is_update_phrase(record['comments'], phrases):

        record['who_code'] = '10'
        record['who_category'] = 'Not of interest'
        record['who_subcategory'] = 'Not of interest'
        record['who_measure'] = 'Not of interest'

    return(record)


def is_update_phrase(comment: str, phrases: list):

    if comment is None:

        return(False)

    res = [bool(re.search(phrase, comment)) for phrase in phrases]

    if sum(res) > 0:

        return(True)

    else:

        return(False)


def financial_measures(record):
    '''
    Function to move values from prov_measure to value_usd for financial reasures.

    prov_measure values are replaced with 1 for coding.

    '''

    financial = ['E3_Fiscal measures',
                 'E4_International support',
                 'H4_Emergency investment in healthcare',
                 'H5_Investment in vaccines']

    if record['prov_category'] in financial:

        record['value_usd'] = record['prov_subcategory']

        record['prov_subcategory'] = 1

    return(record)


def get_comment_links(comments: str):
    '''
    Function to get all links from a comment string

    Returns a list of links
    '''

    exp = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    return(exp.findall(comments))


def assign_comment_links(record: dict):
    '''
    Function to assign links found in comments to links fields
    '''

    links = get_comment_links(record['comments'])

    try:

        record['link'] = links[0]

    except:

        pass

    try:

        record['alt_link'] = links[1]

    except:

        pass

    return(record)
