import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per
from check import check_output
from master.main import get_new_records

argv = sys.argv

create_dir("tmp/master")

logging.basicConfig(
    filename="tmp/master/master.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

print("Reading master data...")
logging.info("Reading master data...")

manually_cleaned = pd.read_csv("tmp/manually_cleaned/records.csv", low_memory=False)

previous_update = pd.read_csv("data/not_cleansed/master_latest.csv", low_memory=False)

update = pd.read_csv("tmp/postprocess/records.csv", low_memory=False)

# Combine with new data (independent from IDs)
print("Combining manually cleaned and update data...")
logging.info("Combining manually cleaned and update data...")

new_records = get_new_records(
    update,
    previous_update,
    ["country_territory_area", "dataset", "area_covered", "who_code", "date_start"],
)

new_records["processed"] = "not_cleansed"

master = pd.concat([manually_cleaned, new_records])

check_output(master)

log_records_per(manually_cleaned, "dataset")
log_records_per(manually_cleaned, "processed")

master.to_csv("tmp/master/master.csv")
print("Success.")
logging.info("Success.")
