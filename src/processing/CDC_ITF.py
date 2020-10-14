"""
CDC_ITF.py
====================================
Transform CDC_ITF records to WHO PHSM format.

**Data Source:**
`https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm <https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm>`_

**Processing Steps:**

1. Generate a blank record with required keys.
2. Move data from provider record to new record with ``apply_key_map`` using key mapping in ``config/key_map/CDC_ITF.csv``.


https://pypi.org/project/countrycode/

"""
import pandas as pd
from countrycode.countrycode import countrycode

# hot fix for sys.path issues in test environment
try:

    from processing import utils
    from processing import check

except Exception as e:

    from src.processing import utils
    from src.processing import check


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame):

    comments = join_comments(record)

    # 1. Create a new blank record
    new_record = utils.generate_blank_record()

    # 2. replace data in new record with data from old record using key_ref
    record = utils.apply_key_map(new_record, record, key_ref)

    # 4. Assign merged comments
    record['comments'] = comments

    # 5. Handle date
    record = utils.parse_date(record)

    # 1. Assign date_end
    record = add_date_end(record)

    # 1. Make manual country name changes
    record = utils.replace_conditional(record, 'country_territory_area', 'Saint Martin', 'French Saint Martin')
    record = utils.replace_conditional(record, 'country_territory_area', 'RÃ©union', 'Reunion')
    record = utils.replace_conditional(record, 'country_territory_area', 'CuraÃ§ao', 'Curacao')
    record = utils.replace_conditional(record, 'country_territory_area', 'St. Barts', 'Saint Barthelemy')
    record = utils.replace_conditional(record, 'country_territory_area', 'Czechia', 'Czech Republic')
    record = utils.replace_conditional(record, 'country_territory_area', 'D. P. R. of Korea', 'North Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Eswatini', 'Swaziland')
    record = utils.replace_conditional(record, 'country_territory_area', 'South Korea', 'Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Bonaire, Saint Eustatius and Saba', 'Carribean Netherlands')

    # replace sensitive country names by ISO (utils)
    record = utils.replace_sensitive_regions(record)

    # assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # check missing ISO
    check.check_missing_iso(record)

    # 9. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 10. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 11. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 1. Replace measure_stage extension
    record = utils.replace_conditional(record, 'measure_stage', 'Extend with same stringency', 'extension')


    return(record)


def add_date_end(record: dict):
    '''Function to make ``date_end`` ``date_start`` if ``measure_stage`` is "Lift"'''

    if record['measure_stage'] == 'Lift':

        record['date_end'] = record['date_start']

    return(record)


def join_comments(record: dict):
    '''Function to combine comments from two provider fields'''

    if type(record['Concise Notes']) != str:

        record['Concise Notes'] = ''

    if type(record['Notes']) != str:

        record['Notes'] = ''

    comments = record['Concise Notes'] + '. ' + record['Notes']

    return(comments)
