"""
preprocess.py
====================================
Script to convert provider datasets individual record dictionaries
"""

import pandas as pd
import logging

from preprocess.utils import df_to_records, write_records

# Source of config file - also move to Makefile when ready

# Dataset sources: these should be in makefile when ready
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
cdc = "raw_data/CDC_ITF_latest.xlsx"
acaps = "raw_data/ACAPS_latest.xlsx"

# replace this with logging
logging.info("Reading JH_HIT...")
jh = pd.read_csv(jh)

jh = df_to_records(jh, "JH_HIT")

print("Reading CDC_ITF...")
cdc = pd.read_excel(cdc, sheet_name='Line list')

cdc = df_to_records(cdc, "CDC_ITF")

print("Reading ACAPS...")
acaps = pd.read_excel(acaps, sheet_name='Dataset')

acaps = df_to_records(acaps, "ACAPS")

# concat all record lists
records = jh + cdc + acaps

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
