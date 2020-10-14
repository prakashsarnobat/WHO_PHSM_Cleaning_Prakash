"""
ACAPS.py
====================================
Transform ACAPS records to WHO PHSM format.

**Data Source:**
`https://www.acaps.org/covid-19-government-measures-dataset <https://www.acaps.org/covid-19-government-measures-dataset>`_

**Processing Steps:**



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

    # 2. Create a new blank record
    new_record = utils.generate_blank_record()

    # 3. replace data in new record with data from old record using key_ref
    record = utils.apply_key_map(new_record, record, key_ref)

    return(record)
