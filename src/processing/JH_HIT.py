"""
JH_HIT.py
====================================
Transform JH_HIT records to WHO PHSM format.

**Data Source:**
`https://github.com/HopkinsIDD/hit-covid <https://github.com/HopkinsIDD/hit-covid>`_

**Processing Steps:**

1. Remove records with null ``locality`` AND null ``usa_county`` values.
2. Generate a blank record with required keys.
3. Move data from provider record to new record with ``apply_key_map`` using key mapping in ``config/key_map/JH_HIT.csv``.
4. Remove a subset of ``prov_measure`` values. See ``config/prov_measure_filter/JH_HIT.csv`` for exact values.
5. Parse date formats in ``date_start``, ``date_end``, ``date_entry``.
6. Assign a unique record ID.
7. Map non-ascii characters to their closest ascii equivalent.
8. Shift sensitive country names to ``area_covered``.
9. Assign ISO codes using ``country_territory_area``.
10. Check for missing ``iso`` codes.
11. Assign WHO-accepted ``country_territory_area``, ``who_region``, ``iso_3166_1_numeric``
12. Assign WHO PHSM dataset coding using ``prov_measure``, ``prov_subcategory``, ``prov_category``
13. Check for missing ``who_code`` values.
14. Replace ``admin_level`` values: null -> 'unknown', 'Yes' -> 'national', 'No' -> 'state'
15. Replace ``prov_measure`` and ``prov_category`` with 'not_enough_to_code' if ``comments`` are blank and ``prov_category`` no 'school_closed'
16. Replace ``non_compliance_penalty`` "non_compliance_penalty" -> "Not Known"

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


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame, prov_measure_filter: pd.DataFrame):

    # 1.
    if pd.isnull(record['locality']) and pd.isnull(record['usa_county']):
        return(None)

    # 2. generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # 3. replace data in new record with data from old record using column
    # reference (shared)
    record = utils.apply_key_map(new_record, record, key_ref)

    # 4.
    record = apply_prov_measure_filter(record, prov_measure_filter)

    # replace with a None - passing decorator
    if record is None:
        return(None)

    # 5. Handle date - infer format (shared)
    record = utils.parse_date(record)

    # 6. Assign unique ID (shared)
    record = utils.assign_id(record)

    # 7. replace non ascii characters (shared)

    # 8. replace sensitive country names by ISO (utils)
    record = utils.replace_sensitive_regions(record)

    # 9. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 10. check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # 11. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 12. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 13. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 14. replace admin_level values
    record = utils.replace_conditional(record, 'admin_level', '', 'unknown')
    record = utils.replace_conditional(record, 'admin_level', 'Yes', 'national')
    record = utils.replace_conditional(record, 'admin_level', 'No', 'state')

    # 15. fill_not_enough_to_code
    record = fill_not_enough_to_code(record)

    # 16. replace unknown non_compliance_penalty
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'unknown', 'Not Known')

    return(record)


def apply_prov_measure_filter(record: dict, prov_measure_filter: pd.DataFrame):
    '''Function to filter only some prov_measure and prov_category values'''

    if record['prov_category'] in list(prov_measure_filter['prov_category']) and record['prov_measure'] in list(prov_measure_filter['prov_measure']):

        return record

    else:

        return(None)


def fill_not_enough_to_code(record: dict):
    '''Function to add "not enough to code" label to specific records'''

    if record['comments'] == '' and record['prov_category'] != 'school_closed':

        record['prov_measure'] = 'not_enough_to_code'
        record['prov_category'] = 'not_enough_to_code'

    return(record)
