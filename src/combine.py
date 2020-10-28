"""
postprocess.py
====================================
Script to combine previously updated data with a new data.
"""

# Import data
import pickle
import sys
import pandas as pd
import logging

from utils import create_dir
from postprocess.main import postprocess
from check import check_output
from combine.main import adjust_manually_cleaned

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

# Combine with new data (independent from IDs)
