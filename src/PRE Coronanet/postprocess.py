"""
postprocess.py
====================================
Script to make manual changes to multiple dataset records.
"""

import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per, log_records_total
from postprocess.main import postprocess
from check import check_output

argv = sys.argv

# Create postprocess directory in tmp
create_dir('tmp/postprocess')

# Setup logging to log into postprocess directory
logging.basicConfig(filename='tmp/postprocess/postprocess.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Read processed records
records = pd.read_csv('tmp/process/records.csv', low_memory = False)

print("Postprocessing Data...")
logging.info("Postprocessing Data...")

# Split dataset into groups by data provider
records = records.groupby('dataset')
records = [records.get_group(x) for x in records.groups]

# List to store datasets after postprocessing
postprocessed = []

# Apply postprocessing changes to each dataset
for data in records:

    postprocessed.append(postprocess(data))

# Recombine all datasets
records = pd.concat(postprocessed)

# Add values to the who_id_original column
records['who_id_original'] = records['who_id']

# Apply standard checks to postprocessed file
check_output(records)

# Log number of records in the postprocessed dataset
log_records_per(records, 'dataset')
log_records_total(records)

# Write postprocess file to csv
records.to_csv('tmp/postprocess/records.csv', index=False)

print("Success.")
logging.info("Success.")
