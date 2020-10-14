"""
JH_HIT.py
====================================
Transform JH_HIT records to WHO PHSM format.

**Data Source:**
`https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm <https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm>`_

**Processing Steps:**

1. 

"""
import pandas as pd

# hot fix for sys.path issues in test environment
try:

    from processing import utils
    from processing import check

except Exception as e:

    from src.processing import utils
    from src.processing import check


def transform(record: dict):

    return(record)
