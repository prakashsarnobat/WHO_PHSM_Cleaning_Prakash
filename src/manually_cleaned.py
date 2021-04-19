"""
manually_cleaned.py

Script to combine previously updated data with a new data.

Preprocessing Mistress should be separate from master creation
"""
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per, log_records_total
from check import check_output
from manually_cleaned.main import adjust_manually_cleaned, columns_to_lower

argv = sys.argv

# Create manually_cleaned directory in tmp
create_dir('tmp/manually_cleaned')

# Setup logging to log into manually_cleaned directory
logging.basicConfig(filename='tmp/manually_cleaned/manually_cleaned.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Reading manually cleaned data...")
logging.info("Reading manually cleaned data...")

# Define columns that should be transformed to lower case
# (these have known coded values)
lowercase_columns = ['admin_level',
                     'enforcement',
                     'keep',
                     'measure_stage',
                     'non_compliance_penalty',
                     'processed',
                     'reason_ended']

# Read manually cleaned data
# Read manually cleaned data
manually_cleaned = pd.read_csv('data/cleansed/mistress_latest.csv', low_memory=False,
    dtype={'date_start':str, 'date_end':str, 'date_entry':str, 'date_processed':str})

#euro = pd.read_excel('data/cleansed/mistress_latest.xlsx', engine='openpyxl',
#                     dtype={'date_start': str,
#                            'date_end': str,
#                            'date_entry': str,
#                            'date_processed': str},
#                    sheet_name=1)
#print(euro.columns)

manually_cleaned = manually_cleaned.rename(columns={"ï»¿processed": "processed"})

print(manually_cleaned.columns)
print(len(manually_cleaned["prop_id"]))
# Parse date values with a specific date format. This will throw an error on unexpected values
#manually_cleaned['date_start'] = pd.to_datetime(manually_cleaned['date_start'], format='%d/%m/%Y')
#manually_cleaned['date_end'] = pd.to_datetime(manually_cleaned['date_end'], format='%d/%m/%Y')
#manually_cleaned['date_entry'] = pd.to_datetime(manually_cleaned['date_entry'], format='%d/%m/%Y')
#manually_cleaned['date_processed'] = pd.to_datetime(manually_cleaned['date_processed'], format='%d/%m/%Y')

# Parse date values with a specific date format. This will throw an error on unexpected values

# manually_cleaned['date_processed'] = pd.to_datetime(manually_cleaned['date_processed'],
#                                                    format='%d/%m/%Y')

print("Checking manually cleaned...")
logging.info("Checking manually cleaned...")

print("Adjusting manually cleaned...")
logging.info("Adjusting manually cleaned...")

# Apply record adjustments to manually cleaned data
manually_cleaned = adjust_manually_cleaned(manually_cleaned)

# update `keep` labels for records coded with who_code in ['10', '11', '12', '13']
manually_cleaned.loc[(pd.isna(manually_cleaned['keep'])) & ([x in ['10', '11', '12', '13'] for x in manually_cleaned['who_code']]), 'keep'] = 'n'
manually_cleaned.loc[(pd.isna(manually_cleaned['keep'])) & ([x not in ['10', '11', '12', '13'] for x in manually_cleaned['who_code']]), 'keep'] = 'y'

print(manually_cleaned.columns)
# Convert defined columns to lower case
manually_cleaned = columns_to_lower(manually_cleaned, lowercase_columns)

# Check manually cleaned data with standard output checks
check_output(manually_cleaned)

# Log number of records in the dataset by group
log_records_per(manually_cleaned, 'dataset')
log_records_per(manually_cleaned, 'processed')
log_records_total(manually_cleaned)

# Write out adjusted data
manually_cleaned.to_csv('tmp/manually_cleaned/records.csv', index=False)

print("Success.")
logging.info("Success.")
