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

from utils import create_dir, log_records_per
from postprocess.main import postprocess
from check import check_output
from combine.main import adjust_manually_cleaned, get_new_records

argv = sys.argv

create_dir('tmp/combine')

logging.basicConfig(filename='tmp/combine/combine.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Combining Data...")
logging.info("Combining Data...")

manually_cleaned = pd.read_csv('data/not_cleansed/mistress_latest.csv')

records = pd.read_csv('tmp/postprocess/records.csv')

print("Checking manually cleaned...")
logging.info("Checking manually cleaned...")

# Check mistress
check_output(manually_cleaned)

print("Adjusting manually cleaned...")
logging.info("Adjusting manually cleaned...")

# Apply changes to mistress
manually_cleaned = adjust_manually_cleaned(manually_cleaned)

log_records_per(manually_cleaned, 'dataset')
log_records_per(manually_cleaned, 'processed')

# Combine with new data (independent from IDs)
new_records = get_new_records(records, manually_cleaned, ['country_territory_area', 'dataset', 'area_covered', 'who_code', 'date_start'])

print(new_records)

master = pd.concat([manually_cleaned, new_records])

print("Success.")
logging.info("Success.")



#log number of records here, number of cleansed etc.
