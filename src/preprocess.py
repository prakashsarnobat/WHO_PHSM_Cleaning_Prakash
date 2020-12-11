"""
:noindex:
preprocess.py
====================================
Script to convert provider datasets individual record dictionaries

Data Sources:
`https://www.acaps.org/covid-19-government-measures-dataset <https://www.acaps.org/covid-19-government-measures-dataset>`_
`https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm <https://www.cdc.gov/mmwr/preview/mmwrhtml/00001590.htm>`_
`https://github.com/HopkinsIDD/hit-covid <https://github.com/HopkinsIDD/hit-covid>`_
`https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv <https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv>`_

"""

import pandas as pd
import logging
from datetime import datetime as dt

from utils import create_dir
from preprocess import utils, check

# Create tmp directory
create_dir('tmp')

# Create preprocess directory in tmp
create_dir('tmp/preprocess')

# Setup logging to log into the preprocess directory
logging.basicConfig(filename='tmp/preprocess/preprocess.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Preprocessing Data...")
logging.info("Preprocessing Data...")

# HOTFIX: limit the number of records that will be ingested from each dataset. Used for development.
# Should be None for production.
record_limit = None

# Define dataset sources
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
cdc = "data/raw/CDC_ITF_latest.csv"
acaps = "data/raw/ACAPS_latest.csv"
oxcgrt = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv"
check_dir = 'config/input_check'

# Filter out previous records for non-oxcgrt datasets
previous_update = pd.read_csv('data/merge/update_merge_2020_12_02.csv')

# Split previous update by dataset
previous_update = utils.split_df_by_group(previous_update, 'dataset')

# Load accepted column reference
column_config = {'JH_HIT':pd.read_csv(check_dir + '/columns/JH_HIT.csv'),
                 'CDC_ITF':pd.read_csv(check_dir + '/columns/CDC_ITF.csv'),
                 'ACAPS':pd.read_csv(check_dir + '/columns/ACAPS.csv'),
                 'OXCGRT':pd.read_csv(check_dir + '/columns/OXCGRT.csv')}

# Load accepted date format reference
date_config = pd.read_csv(check_dir + '/date_format/date_format.csv')

# Read JH_HIT Data
jh = pd.read_csv(jh)

# Remove records that have already been processed
jh = utils.remove_processed_records(jh, previous_update['JH_HIT'], 'unique_id', 'prop_id')

# Check JH_HIT Data
check.check_input(records=jh,
                  column_config=column_config['JH_HIT'],
                  date_config=date_config,
                  dataset = 'JH_HIT')

# Convert JH_HIT data to list of record dicts
jh = utils.df_to_records(jh, "JH_HIT")

# Log the number of JH_HIT records
logging.info("JH_HIT_RECORDS=%d" % len(jh))

# Read CDC_ITF data
cdc = pd.read_csv(cdc,
                  dtype={'Date implemented or lifted':str, 'Date Entered':str})

# Remove records that have already been processed
cdc = utils.remove_processed_records(cdc, previous_update['CDC_ITF'], 'Unique Identifier', 'prop_id')

# Parse CDC_ITF date format
cdc["Date implemented or lifted"] = pd.to_datetime(cdc["Date implemented or lifted"], format='%d/%m/%Y')
cdc["Date Entered"] = pd.to_datetime(cdc["Date Entered"], format='%d/%m/%Y')

# Check CDC_ITF Data
check.check_input(records=cdc,
                  column_config=column_config['CDC_ITF'],
                  date_config=date_config,
                  dataset = 'CDC_ITF')

# Convert CDC_ITF data to list of record dicts
cdc = utils.df_to_records(cdc, "CDC_ITF")

# Log the number of CDC_ITF records
logging.info("CDC_ITF_RECORDS=%d" % len(cdc))

# Read ACAPS Data
acaps = pd.read_csv(acaps,
                    parse_dates = ['DATE_IMPLEMENTED', 'ENTRY_DATE'],
                    dayfirst = True)

# Remove records that have already been processed
acaps = utils.remove_processed_records(acaps, previous_update['ACAPS'], 'ID', 'prop_id')

# Check ACAPS Data
check.check_input(records=acaps,
                  column_config=column_config['ACAPS'],
                  date_config=date_config,
                  dataset='ACAPS')

# Convert ACAPS data to list of record dicts
acaps = utils.df_to_records(acaps, "ACAPS")

# Log the number of ACAPS records
logging.info("ACAPS_RECORDS=%d" % len(acaps))

# Read OXCGRT Data
oxcgrt = pd.read_csv(oxcgrt, parse_dates=["Date"], low_memory=False)

# Check OXCGRT Data
check.check_input(records=oxcgrt,
                  column_config=column_config['OXCGRT'],
                  date_config=date_config,
                  dataset = 'OXCGRT')

# Define columns that will be dropped from OXCGRT data
drop_columns = ['ConfirmedCases',
               'ConfirmedDeaths', 'StringencyIndex', 'StringencyIndexForDisplay',
               'StringencyLegacyIndex', 'StringencyLegacyIndexForDisplay',
               'GovernmentResponseIndex', 'GovernmentResponseIndexForDisplay',
               'ContainmentHealthIndex', 'ContainmentHealthIndexForDisplay',
               'EconomicSupportIndex', 'EconomicSupportIndexForDisplay']

# Drop defined columns from OXCGRT data
oxcgrt.drop(drop_columns, axis = 1, inplace = True)

# Replace NA values with 0.0
oxcgrt.fillna(0.0, inplace = True)

# Convert OxCGRT data to list of record dicts
oxcgrt = utils.df_to_records(oxcgrt, "OXCGRT", drop_columns)

# Log the number of OXCGRT records
logging.info("OXCGRT_RECORDS=%d" % len(oxcgrt))

# concat all record lists - filter each by the (development only) record limit
records = jh[:record_limit] + cdc[:record_limit] + acaps[:record_limit] + oxcgrt[:record_limit]

# write list of record dicts to a pickle file
utils.write_records(records, "tmp/preprocess", "records.pickle")
logging.info("TOTAL_INPUT_RECORDS=%d" % len(records))

print("Success.")
logging.info("Success.")
