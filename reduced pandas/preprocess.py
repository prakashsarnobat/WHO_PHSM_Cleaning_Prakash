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
`https://who.maps.arcgis.com/apps/opsdashboard/index.html#/ead3c6475654481ca51c248d52ab9c61 <https://who.maps.arcgis.com/apps/opsdashboard/index.html#/ead3c6475654481ca51c248d52ab9c61>`_
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
# Allows ingestion hashes to be saved - should be True in production, not in development
save_ingestion_hashes = False

# Original web-based Data sources for Oxford and JH:
# https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv
# https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv

# DEFINE DATASET SOURCES
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"
cdc = "data/raw/CDC_ITF_210602.csv"
acaps = "data/raw/ACAPS_latest.csv"
oxcgrt = "data/raw/OxCGRT_latest_withnotes.csv"
euro = "data/raw/diff_EURO.xlsx"
check_dir = 'config/input_check'

# Load accepted column reference
column_config = {'JH_HIT': pd.read_csv(check_dir + '/columns/JH_HIT.csv'),
                 'CDC_ITF': pd.read_csv(check_dir + '/columns/CDC_ITF.csv'),
                 'ACAPS': pd.read_csv(check_dir + '/columns/ACAPS.csv'),
                 'OXCGRT': pd.read_csv(check_dir + '/columns/OXCGRT.csv'),
                 'EURO': pd.read_csv(check_dir + '/columns/EURO.csv')}

# Load accepted date format reference
date_config = pd.read_csv(check_dir + '/date_format/date_format.csv')

ingestion_hashes = {'JH_HIT': 'config/ingestion_hashes/JH_HIT.csv',
                    'CDC_ITF': 'config/ingestion_hashes/CDC_ITF.csv',
                    'OXCGRT': 'config/ingestion_hashes/OXCGRT.csv',
                    'ACAPS': 'config/ingestion_hashes/ACAPS.csv',
                    'EURO': 'config/ingestion_hashes/EURO.csv'}


# Read EURO Data
"""
euro = pd.read_csv(euro,
                   parse_dates=["Start of measure", "End of measure"],
                   low_memory=False,
                   dtype={'Category': str,
                          'Subcategory': str,
                          'Measure': str})
"""

euro = pd.read_excel(euro, engine='openpyxl',
                     dtype={'Category': str,
                            'Subcategory': str,
                            'Measure': str},
                    sheet_name=0)
print(euro.columns)

# Convert EURO columns to str
euro.columns = euro.columns.astype("str")

# Remove records that have already been processed
euro = utils.filter_new_hashes(euro, ingestion_hashes['EURO'],
                               save_ingestion_hashes=save_ingestion_hashes)

# Check EURO Data
check.check_input(records=euro,
                  column_config=column_config['EURO'],
                  date_config=date_config,
                  dataset='EURO')

euro = euro.fillna('')

# Convert EURO data to list of record dicts
euro = utils.df_to_records(euro, "EURO")

# Log the number of EUROrecords
logging.info("EURO_RECORDS=%d" % len(euro))

# Read OXCGRT Data
oxcgrt = pd.read_csv(oxcgrt, parse_dates=["Date"], low_memory=False)

# Remove records that have already been processed
oxcgrt = utils.filter_new_hashes(oxcgrt, ingestion_hashes['OXCGRT'], save_ingestion_hashes=save_ingestion_hashes)

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
oxcgrt.drop(drop_columns, axis=1, inplace=True)

# Replace NA values with 0.0
oxcgrt.fillna(0.0, inplace=True)

# Convert OxCGRT data to list of record dicts
oxcgrt = utils.df_to_records(oxcgrt, "OXCGRT", drop_columns)

# Log the number of OXCGRT records
logging.info("OXCGRT_RECORDS=%d" % len(oxcgrt))

# concat all record lists - filter each by the (development only) record limit
records = euro[:record_limit] + \
          oxcgrt[:record_limit]

# write list of record dicts to a pickle file
utils.write_records(records, "tmp/preprocess", "records.pickle")
logging.info("TOTAL_INPUT_RECORDS=%d" % len(records))

print("Success.")
logging.info("Success.")
