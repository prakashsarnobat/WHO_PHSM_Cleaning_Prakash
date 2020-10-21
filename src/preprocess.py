"""
preprocess.py
====================================
Script to convert provider datasets individual record dictionaries
"""

import pandas as pd
import logging

from utils import create_dir
from preprocess import utils, check

create_dir('tmp')
create_dir('tmp/preprocess')

# Source of config file - also move to Makefile when ready
logging.basicConfig(filename='tmp/preprocess/preprocess.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Preprocessing Data...")
logging.info("Preprocessing Data...")

# Dataset sources: these should be in makefile when ready
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
cdc = "raw_data/CDC_ITF_latest.xlsx"
acaps = "raw_data/ACAPS_latest.xlsx"
check_dir = 'config/input_check'

# Load column config
column_config = {'JH_HIT':pd.read_csv(check_dir + '/columns/JH_HIT.csv'),
                 'CDC_ITF':pd.read_csv(check_dir + '/columns/CDC_ITF.csv'),
                 'ACAPS':pd.read_csv(check_dir + '/columns/ACAPS.csv')}

jh = pd.read_csv(jh)

check.check_input(records=jh,
                  column_config=column_config['JH_HIT'])

jh = utils.df_to_records(jh, "JH_HIT")

logging.info("JH_HIT_RECORDS=%d" % len(jh))

cdc = pd.read_excel(cdc, sheet_name='Line list')

check.check_input(records=cdc,
                  column_config=column_config['CDC_ITF'])

cdc = utils.df_to_records(cdc, "CDC_ITF")

logging.info("CDC_ITF_RECORDS=%d" % len(cdc))

acaps = pd.read_excel(acaps, sheet_name='Dataset')

check.check_input(records=acaps,
                  column_config=column_config['ACAPS'])

acaps = utils.df_to_records(acaps, "ACAPS")

logging.info("ACAPS_RECORDS=%d" % len(acaps))

# concat all record lists
records = jh + cdc + acaps

# write list to a pickle file
utils.write_records(records, "tmp/preprocess", "records.pickle")
logging.info("INPUT_RECORDS=%d" % len(records))

# replace this with logging
print("Success.")
logging.info("Success.")

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
