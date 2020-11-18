import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per
from check import check_output
from master.main import get_new_records

argv = sys.argv
pd.set_option('display.max_columns', 500)

create_dir("tmp/master")

logging.basicConfig(
    filename="tmp/master/master.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

print("Reading master data...")
logging.info("Reading master data...")

manually_cleaned = pd.read_csv("tmp/manually_cleaned/records.csv", low_memory=False, parse_dates = ['date_start'])

print("Reading previous update...")
logging.info("Reading previous update...")

previous_update = pd.read_csv("data/not_cleansed/update_latest_new.csv", low_memory=False, parse_dates = ['date_start'], encoding='latin1')

update = pd.read_csv("tmp/postprocess/records.csv", low_memory=False, parse_dates = ['date_start'])

# Combine with new data (independent from IDs)
print("Combining manually cleaned and update data...")
logging.info("Combining manually cleaned and update data...")

combo_cols = ["country_territory_area", "dataset", "area_covered", "who_code", "date_start"]

print(previous_update[['prop_id'] + combo_cols].loc[(previous_update['dataset'] == 'OXCGRT'), :])
print(update[['prop_id'] + combo_cols].loc[(update['dataset'] == 'OXCGRT'), :])

new_ids = set(update['prop_id']).difference(set(previous_update['prop_id']))

print('THESE ARE THE NEW IDs')
print(len(new_ids))
#print([x in new_ids for x in update['prop_id']])
#print(update.loc[[x in new_ids for x in update['prop_id']], 'dataset'].value_counts())

new_records = get_new_records(
    update,
    previous_update,
    combo_cols,
)

print(new_records)
new_records.to_csv('tmp/new_records.csv')

new_records["processed"] = "not_cleansed"

master = pd.concat([manually_cleaned, new_records])

check_output(master)

log_records_per(master, "dataset")
log_records_per(master, "processed")

master.to_csv("tmp/master/master.csv")
print("Success.")
logging.info("Success.")
