import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per
from postprocess.main import postprocess
from check import check_output
from master.main import get_new_records

argv = sys.argv

create_dir('tmp/master')

logging.basicConfig(filename='tmp/master/master.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

print("Reading master data...")
logging.info("Reading master data...")

manually_cleaned = pd.read_csv('tmp/manually_cleaned/records.csv')

update = pd.read_csv('tmp/postprocess/records.csv')

# Combine with new data (independent from IDs)
print("Combining manually cleaned and update data...")
logging.info("Combining manually cleaned and update data...")

new_records = get_new_records(update, manually_cleaned, ['country_territory_area', 'dataset', 'area_covered', 'who_code', 'date_start'])

master = pd.concat([manually_cleaned, new_records])

check_output(master)

log_records_per(manually_cleaned, 'dataset')
log_records_per(manually_cleaned, 'processed')

master.to_csv('tmp/master/master.csv')
print("Success.")
logging.info("Success.")
