"""
preprocess.py
====================================
Script to convert provider datasets individual record dictionaries
"""

import pandas as pd
import logging
from datetime import datetime as dt

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

#Record limit for development. Should be None for production.
record_limit = None

# Dataset sources: these should be in makefile when ready
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
cdc = "data/raw/CDC_ITF_latest.csv"
acaps = "data/raw/ACAPS_latest.csv"
oxcgrt = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv"
check_dir = 'config/input_check'

# Load column config
column_config = {'JH_HIT':pd.read_csv(check_dir + '/columns/JH_HIT.csv'),
                 'CDC_ITF':pd.read_csv(check_dir + '/columns/CDC_ITF.csv'),
                 'ACAPS':pd.read_csv(check_dir + '/columns/ACAPS.csv'),
                 'OXCGRT':pd.read_csv(check_dir + '/columns/OXCGRT.csv')}

date_config = pd.read_csv(check_dir + '/date_format/date_format.csv')

# Read JH Data
jh = pd.read_csv(jh)

# Check JH Data
check.check_input(records=jh,
                  column_config=column_config['JH_HIT'],
                  date_config=date_config,
                  dataset = 'JH_HIT')

jh = utils.df_to_records(jh, "JH_HIT")

logging.info("JH_HIT_RECORDS=%d" % len(jh))

# Read CDC Data

cdc = pd.read_csv(cdc,
                  dtype={'Date implemented or lifted':str, 'Date Entered':str})

#print(cdc["Date implemented or lifted"])
cdc["Date implemented or lifted"] = pd.to_datetime(cdc["Date implemented or lifted"], format='%d/%m/%Y')
cdc["Date Entered"] = pd.to_datetime(cdc["Date Entered"], format='%d/%m/%Y')

# Check CDC Data
check.check_input(records=cdc,
                  column_config=column_config['CDC_ITF'],
                  date_config=date_config,
                  dataset = 'CDC_ITF')

cdc = utils.df_to_records(cdc, "CDC_ITF")

logging.info("CDC_ITF_RECORDS=%d" % len(cdc))

# Read ACAPS Data
acaps = pd.read_csv(acaps,
                    parse_dates = ['DATE_IMPLEMENTED', 'ENTRY_DATE'],
                    dayfirst = True)

# Check ACAPS Data
check.check_input(records=acaps,
                  column_config=column_config['ACAPS'],
                  date_config=date_config,
                  dataset='ACAPS')

acaps = utils.df_to_records(acaps, "ACAPS")

logging.info("ACAPS_RECORDS=%d" % len(acaps))

# Read OXCGRT Data
oxcgrt = pd.read_csv(oxcgrt, parse_dates=["Date"], low_memory=False)

# Check OXCGRT Data
check.check_input(records=oxcgrt,
                  column_config=column_config['OXCGRT'],
                  date_config=date_config,
                  dataset = 'OXCGRT')

drop_columns = ['ConfirmedCases',
       'ConfirmedDeaths', 'StringencyIndex', 'StringencyIndexForDisplay',
       'StringencyLegacyIndex', 'StringencyLegacyIndexForDisplay',
       'GovernmentResponseIndex', 'GovernmentResponseIndexForDisplay',
       'ContainmentHealthIndex', 'ContainmentHealthIndexForDisplay',
       'EconomicSupportIndex', 'EconomicSupportIndexForDisplay']

oxcgrt.drop(drop_columns, axis = 1, inplace = True)

oxcgrt.fillna(0.0, inplace = True)

oxcgrt = utils.df_to_records(oxcgrt, "OXCGRT", drop_columns)

logging.info("OXCGRT_RECORDS=%d" % len(oxcgrt))

# concat all record lists
records = jh[:record_limit] + cdc[:record_limit] + acaps[:record_limit] + oxcgrt[:record_limit]

# write list to a pickle file
utils.write_records(records, "tmp/preprocess", "records.pickle")
logging.info("TOTAL_INPUT_RECORDS=%d" % len(records))

# replace this with logging
print("Success.")
logging.info("Success.")
