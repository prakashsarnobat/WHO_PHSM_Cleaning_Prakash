"""
CDC_ITF.py
====================================
Transform CDC_ITF records to WHO PHSM format.

**Data Source:**
`https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm <https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm>`_

**Processing Steps:**

1. Join comments in ``Concise Notes`` and ``Notes`` columns
2. Generate a blank record with required keys.
3. Move data from provider record to new record with ``apply_key_map`` using key mapping in ``config/key_map/CDC_ITF.csv``.
4. Assign merged comments to new record.
5. Handle date formatting.
6. Assign ``date_end`` equal to ``date_start`` if ``measure_stage`` == "Lift".
7. Make manual country name changes.
8. Replace sensitive country names.
9. Assign ISO code.
10. Check for missing ISO codes.
11. Join WHO accepted country names (shared).
12. Join who coding from lookup (shared).
13. Check for missing WHO codes (shared).
14. Replace non-specific area_covered value.
15. Replace measure_stage extension.
16. Add WHO PHSM admin_level values.

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

    # 1. Join comments in ``Concise Notes`` and ``Notes`` columns
    comments = join_comments(record)

    # 2. Create a new blank record
    new_record = utils.generate_blank_record()

    # 3. replace data in new record with data from old record using key_ref
    record = utils.apply_key_map(new_record, record, key_ref)

    # 4. Assign merged comments to new record
    record['comments'] = comments

    # 6. Assign unique ID (shared)
    #record = utils.assign_id(record)

    # If area_covered is national, set to blank
    record = area_covered_national(record)

    # 5. Handle date formatting
    record = utils.parse_date(record)

    # 6. Assign date_end with measure_stage value
    record = add_date_end(record)

    # 7. Make manual country name changes
    record = utils.replace_conditional(record, 'country_territory_area', 'Saint Martin', 'French Saint Martin')
    record = utils.replace_conditional(record, 'country_territory_area', 'RÃ©union', 'Reunion')
    record = utils.replace_conditional(record, 'country_territory_area', 'CuraÃ§ao', 'Curacao')
    record = utils.replace_conditional(record, 'country_territory_area', 'St. Barts', 'Saint Barthelemy')
    record = utils.replace_conditional(record, 'country_territory_area', 'Czechia', 'Czech Republic')
    record = utils.replace_conditional(record, 'country_territory_area', 'D. P. R. of Korea', 'North Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Eswatini', 'Swaziland')
    record = utils.replace_conditional(record, 'country_territory_area', 'South Korea', 'Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Bonaire, Saint Eustatius and Saba', 'Carribean Netherlands')

    # 7. Make manual measure_stage name changes
    record = utils.replace_conditional(record, 'measure_stage', 'Impose', 'new')
    record = utils.replace_conditional(record, 'measure_stage', 'Lift', 'phase-out')
    record = utils.replace_conditional(record, 'measure_stage', 'Pause', 'modification')
    record = utils.replace_conditional(record, 'measure_stage', 'Ease', 'modification')
    record = utils.replace_conditional(record, 'measure_stage', 'Strengthen', 'modification')

    # 7. Make manual non_compliance_penalty name changes
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Yes', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Yes ', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'yes ', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'yes', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'No', None)
    record = utils.replace_conditional(record, 'non_compliance_penalty', "No'", None)

    # 8. replace sensitive country names
    record = utils.replace_sensitive_regions(record)

    # 9. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 10. check missing ISO
    check.check_missing_iso(record)

    # 11. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 12. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 13. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 14. set all admin_level values to national
    record = utils.replace_conditional(record, 'admin_level', 'Subnational/regional only', 'national')
    record = utils.replace_conditional(record, 'admin_level', 'subnational/regional only', 'national')
    record = utils.replace_conditional(record, 'admin_level', 'National', 'national')

    # 15. Replace measure_stage extension
    record = utils.replace_conditional(record, 'measure_stage', 'Extend with same stringency', 'extension')

    # 16. Add WHO PHSM admin_level values
    record = utils.add_admin_level(record)

    record = utils.remove_tags(record, ['comments', 'link', 'alt_link'])

    return(record)


def area_covered_national(record: dict):
    '''
    Function to remove area_covered == "national"

    Replace with None
    '''

    if record['area_covered'] in ['national']:

        record['area_covered'] = None

    return(record)


def add_date_end(record: dict):
    '''Function to make ``date_end`` ``date_start`` if ``measure_stage`` is "Lift"'''

    if record['measure_stage'] == 'Lift':

        record['date_end'] = record['date_start']

    return(record)


def join_comments(record: dict):
    '''Function to combine comments from "Concise Notes" and "Notes" fields'''

    if type(record['Concise Notes']) != str:

        record['Concise Notes'] = ''

    if type(record['Notes']) != str:

        record['Notes'] = ''

    comments = record['Concise Notes'] + '. ' + record['Notes']

    return(comments)
