"""
ACAPS.py
====================================
Transform ACAPS records to WHO PHSM format.

**Data Source:**
`https://www.acaps.org/covid-19-government-measures-dataset <https://www.acaps.org/covid-19-government-measures-dataset>`_

**Processing Steps:**

1. Create a new blank record
2. replace data in new record with data from old record using key_ref
3. Make manual country name changes
4. replace sensitive country names by ISO (utils)
5. assign ISO code
6. check for missing ISO codes (shared)
7. Join WHO accepted country names (shared)
8. Add WHO PHSM admin_level values

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

    # 1. Create a new blank record
    new_record = utils.generate_blank_record()

    # 2. replace data in new record with data from old record using key_ref
    record = utils.apply_key_map(new_record, record, key_ref)

    # 6. Assign unique ID (shared)
    record = utils.assign_id(record)

    # 3. Make manual country name changes
    record = utils.replace_conditional(record, 'country_territory_area', 'DRC', 'Democratic Republic of the Congo')
    record = utils.replace_conditional(record, 'country_territory_area', 'CAR', 'Central African Republic')
    record = utils.replace_conditional(record, 'country_territory_area', 'DPRK', 'North Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Eswatini', 'Swaziland')

    # 4. replace sensitive country names by ISO (utils)
    record = utils.replace_sensitive_regions(record)

    # 5. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 6. check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # 7. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 8. Add WHO PHSM admin_level values
    record = utils.add_admin_level(record)

    return(record)
