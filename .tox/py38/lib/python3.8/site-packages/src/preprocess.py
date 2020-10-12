"""
preprocess.py
====================================
Script to convert provider datasets individual record dictionaries
"""

import pandas as pd

from preprocess.utils import df_to_records, write_records

# Source of config file - also move to Makefile when ready

# Dataset sources: these should be in makefile when ready
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"

# replace this with logging
print("Reading JH...")
jh = pd.read_csv(jh)

jh = df_to_records(jh, "JH_HIT")

# concat all record lists
records = jh + []

# write list to a pickle file
write_records(records, "preprocess", "records.pickle")

# replace this with logging
print("Success.")

# concat all record lists together here - write out to a pickle in a tmp
# directory - recover and clean up from error

# Need a function that can accept any dict - use its dataset attribute and
# apply the correct mapper
# Each mapper will rely on some common functions shared between them all
# each mapper will return the record(s) with new ID as a dict with the correct
# column names
# these are combined into final dataset

# each mapper uses a pattern like: rearrange columns, fix country names,
# manual changes
# get docs working
