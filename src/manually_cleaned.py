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
from manually_cleaned.main import adjust_manually_cleaned

argv = sys.argv

create_dir('tmp/manually_cleaned')

logging.basicConfig(filename='tmp/manually_cleaned/manually_cleaned.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Reading manually cleaned data...")
logging.info("Reading manually cleaned data...")

manually_cleaned = pd.read_csv('data/cleansed/mistress_latest.csv', low_memory=False)

print("Checking manually cleaned...")
logging.info("Checking manually cleaned...")

print("Adjusting manually cleaned...")
logging.info("Adjusting manually cleaned...")

# Apply changes to mistress
manually_cleaned = adjust_manually_cleaned(manually_cleaned)

# Check mistress
check_output(manually_cleaned)

log_records_per(manually_cleaned, 'dataset')
log_records_per(manually_cleaned, 'processed')

manually_cleaned.to_csv('tmp/manually_cleaned/records.csv', index=False)


print("Success.")
logging.info("Success.")



#log number of records here, number of cleansed etc.
