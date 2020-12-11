import pickle
import sys
import pandas as pd
import logging

from utils import create_dir, log_records_per, log_records_total
from check import check_output
from master.main import get_new_records

argv = sys.argv
pd.set_option('display.max_columns', 5)

# Create master directory in tmp
create_dir("tmp/master")

# Setup logging to log into master directory
logging.basicConfig(
    filename="tmp/master/master.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

print("Reading master data...")
logging.info("Reading master data...")

# Read adjusted manually cleaned data
manually_cleaned = pd.read_csv("tmp/manually_cleaned/records.csv", low_memory=False, parse_dates = ['date_start'])

print("Reading previous update...")
logging.info("Reading previous update...")

# Read previous update data
previous_update = pd.read_csv("data/merge/update_merge_2020_12_09.csv", parse_dates=['date_start'], low_memory=False, encoding='latin1',
                              dtype={'date_start':str})

# Read new update data
update = pd.read_csv("tmp/postprocess/records.csv", low_memory=False, parse_dates = ['date_start'])

print("Combining manually cleaned and update data...")
logging.info("Combining manually cleaned and update data...")

# Define columns to be used for mergign OXCGRT records
combo_cols = ["country_territory_area", "dataset", "area_covered", "who_code", "date_start"]

# Define columns to be dropped from released data
drop_cols = ['processed', 'keep', 'duplicate_record_id', 'prov_category', 'prov_subcategory',
    'prov_measure', 'value_usd', 'percent_interest', 'source_alt', 'queries_comments', 'date_processed']

# Extract previous_update records not from OXCGRT dataset
previous_update_not_ox = previous_update.loc[(previous_update['dataset'] != 'OXCGRT'), :]

# Extract update records not from OXCGRT dataset
update_not_ox = update.loc[(update['dataset'] != 'OXCGRT'), :]

# Extract previous_update records from OXCGRT dataset
previous_update_ox = previous_update.loc[(previous_update['dataset'] == 'OXCGRT'), :]

# Extract update records from OXCGRT dataset
update_ox = update.loc[(update['dataset'] == 'OXCGRT'), :]

# Check that records are not being dropped
assert (len(previous_update_not_ox.index) + len(previous_update_ox.index)) == len(previous_update.index)
assert (len(update_not_ox.index) + len(update_ox.index)) == len(update.index)

# Identify new record sin OXCGRT data
new_records_ox = get_new_records(
    update_ox,
    previous_update_ox,
    combo_cols,
)

# Identify new prop_id values for non-OXCGRT datasets
new_ids = set(update_not_ox['prop_id']).difference(set(previous_update_not_ox['prop_id']))

# Drop NA id values
new_ids = [x for x in new_ids if not pd.isna(x)]

# Identify new records in non-OXCGRT data by which prop_ids are new
new_records_not_ox = update.loc[[x in new_ids for x in update['prop_id']], :]

# concat all new records
new_records = pd.concat([new_records_not_ox, new_records_ox])

# Write new records to csv file - this is probably unnecessary
new_records.to_csv('tmp/new_records.csv')

# Label new records as not_cleansed
new_records["processed"] = "not_cleansed"

# Label all new records with keep == "y"
new_records["keep"] = "y"

# Label new records with who_code in ['10', '11', '12', '13'] as keep == "n"
new_records.loc[[x in ['10', '11', '12', '13'] for x in new_records['who_code']], 'keep'] = "n"

# Assign date processed to today
new_records["date_processed"] = pd.to_datetime('today').strftime('%d-%m-%Y')

# Combine new records with manually_cleaned data
master = pd.concat([manually_cleaned, new_records])

'''

#####

manual steps here

For changes that only occur on a single week

#####

- these should be kept to a bare minimum, should be
  temporary, and should be added with justification & date in comment

'''


'''

#####

End of manual steps

#####

'''

# Apply standard checks to new master file
check_output(master)

# Log number of records in the master dataset
log_records_per(master, "dataset")
log_records_per(master, "processed")
log_records_total(master)

# Write master file to csv
master.to_csv("tmp/master/master.csv", index=False)

# Store a record of IDs and uuids
master[['uuid', 'who_id']].to_csv('tmp/master/id_ref.csv', index=False)

# Filter data to create release dataset
master = master.loc[(master['processed'] == 'sequenced') & (master['keep'] == 'y')]

# Drop defined columns from release data
master.drop(drop_cols, axis=1, inplace=True)

# Write release data to csv
master.to_csv("tmp/master/release.csv", index=False)

print("Success.")
logging.info("Success.")
