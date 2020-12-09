"""
postprocess.py
====================================
Script to combine previously updated data with a new data.

Preprocessing Mistress should be separate from master creation
"""

# Import data
import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per, log_records_total
from postprocess.main import postprocess
from check import check_output
from manually_cleaned.main import adjust_manually_cleaned, columns_to_lower

argv = sys.argv

create_dir('tmp/manually_cleaned')

logging.basicConfig(filename='tmp/manually_cleaned/manually_cleaned.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Reading manually cleaned data...")
logging.info("Reading manually cleaned data...")

lowercase_columns = ['admin_level',
                     'enforcement',
                     'keep',
                     'measure_stage',
                     'non_compliance_penalty',
                     'processed',
                     'reason_ended']

manually_cleaned = pd.read_csv('data/cleansed/mistress_latest.csv', low_memory=False,
    dtype={'date_start':str, 'date_end':str, 'date_entry':str})

manually_cleaned['date_start'] = pd.to_datetime(manually_cleaned['date_start'], format='%d/%m/%Y')
manually_cleaned['date_end'] = pd.to_datetime(manually_cleaned['date_end'], format='%d/%m/%Y')
manually_cleaned['date_entry'] = pd.to_datetime(manually_cleaned['date_entry'], format='%d/%m/%Y')
manually_cleaned['date_processed'] = pd.to_datetime(manually_cleaned['date_processed'], format='%d/%m/%Y')

print("Checking manually cleaned...")
logging.info("Checking manually cleaned...")

print("Adjusting manually cleaned...")
logging.info("Adjusting manually cleaned...")

# Apply changes to mistress
manually_cleaned = adjust_manually_cleaned(manually_cleaned)

manually_cleaned.loc[(pd.isna(manually_cleaned['keep'])) & ([x in ['10', '11', '12', '13'] for x in manually_cleaned['who_code']]), 'keep'] = 'n'
manually_cleaned.loc[(pd.isna(manually_cleaned['keep'])) & ([x not in ['10', '11', '12', '13'] for x in manually_cleaned['who_code']]), 'keep'] = 'y'

manually_cleaned = columns_to_lower(manually_cleaned, lowercase_columns)

# Check mistress
check_output(manually_cleaned)

log_records_per(manually_cleaned, 'dataset')
log_records_per(manually_cleaned, 'processed')
log_records_total(manually_cleaned)

manually_cleaned.to_csv('tmp/manually_cleaned/records.csv', index=False)


print("Success.")
logging.info("Success.")



#log number of records here, number of cleansed etc.
