"""
JH_HIT.py
====================================
Transform JH_HIT records to WHO PHSM format.

**Data Source:**
`https://github.com/HopkinsIDD/hit-covid <https://github.com/HopkinsIDD/hit-covid>`_

**Processing Steps:**

1. Remove records with null ``locality`` AND null ``usa_county`` values.
2. Remove a subset of ``prov_measure`` values. See ``config/prov_measure_filter/JH_HIT.csv`` for exact values.
3. Generate a blank record with required keys.
4. Move data from provider record to new record with ``apply_key_map`` using key mapping in ``config/key_map/JH_HIT.csv``.
5. Parse date formats in ``date_start``, ``date_end``, ``date_entry``.
6. Assign a unique record ID.
7. Map non-ascii characters to their closest ascii equivalent.
8. Check for missing ``iso`` codes.
9. Assign WHO-accepted ``country_territory_area``, ``who_region``, ``iso_3166_1_numeric``
10. Assign WHO PHSM dataset coding using ``prov_measure``, ``prov_subcategory``, ``prov_category``
11. Check for missing ``who_code`` values.
12. Custom JH things (development in progress)

"""
import pandas as pd
from processing import utils
from processing import check


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame, prov_measure_filter: pd.DataFrame):

    # 1.
    if pd.isnull(record['locality']) and pd.isnull(record['usa_county']):
        return(None)

    # 3. generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # 4. replace data in new record with data from old record using column
    # reference (shared)
    record = utils.apply_key_map(new_record, record, key_ref)

    # 2.
    record = apply_prov_measure_filter(record, prov_measure_filter)

    # replace with a None - passing decorator
    if record is None:
        return(None)

    # 5. Handle date - infer format (shared)
    record = utils.parse_date(record)

    # 6. Assign unique ID (shared)
    record = utils.assign_id(record)

    # 7. replace non ascii characters (shared)

    # 8. check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # 9. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 10. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 11. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 12. custom JH things here

    return(record)

def apply_prov_measure_filter(record: dict, prov_measure_filter: pd.DataFrame):
    '''Function to filter only some prov_measure and prov_category values'''

    if record['prov_category'] in list(prov_measure_filter['prov_category']) and record['prov_measure'] in list(prov_measure_filter['prov_measure']):

        return record

    else:

        return(None)
