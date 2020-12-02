"""
process.py
====================================
Script to apply dataset-specific transformers to individual dataset records.
"""

import pickle
import sys
import pandas as pd
import logging
from progress.bar import Bar

from processing.main import process
from processing.utils import generate_blank_record, assign_id, get_min_id
from utils import create_dir, log_records_per, log_records_total
from processing import check
from check import check_output

argv = sys.argv

create_dir('tmp/process')

logging.basicConfig(filename='tmp/process/process.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Processing Data...")

fn = "tmp/preprocess/records.pickle"

records = pickle.load(open(fn, "rb"))

# load key transformation reference
key_ref = {'JH_HIT': pd.read_csv('config/key_map/JH_HIT.csv').to_dict(orient='records'),
           'CDC_ITF': pd.read_csv('config/key_map/CDC_ITF.csv').to_dict(orient='records'),
           'ACAPS': pd.read_csv('config/key_map/ACAPS.csv').to_dict(orient='records'),
           'OXCGRT': pd.read_csv('config/key_map/OXCGRT.csv').to_dict(orient='records')}

# load who country name reference
country_ref = pd.read_csv('config/country_names/who_country_names.csv')

#load who dataset coding
who_coding = {'JH_HIT': pd.read_csv('config/who_coding/JH_HIT.csv').fillna(''),
              'CDC_ITF': pd.read_csv('config/who_coding/CDC_ITF.csv').fillna(''),
              'ACAPS': pd.read_csv('config/who_coding/ACAPS.csv').fillna(''),
              'OXCGRT': pd.read_csv('config/who_coding/OXCGRT.csv').fillna('')}

prov_measure_filter = {'JH_HIT': pd.read_csv('config/prov_measure_filter/JH_HIT.csv')}

no_update_phrase = {'OXCGRT': pd.read_csv('config/no_update_phrase/OXCGRT.csv')}

min_id = get_min_id('data/cleansed/mistress_latest.csv', id_column='who_id')

blank_record = generate_blank_record()

processed_records = []

bar = Bar('Processing Data...', max=len(records))
for record in records:

    record = process(record, key_ref, country_ref, who_coding, prov_measure_filter, no_update_phrase)

    check.check_record_keys_agree(record, blank_record)

    if record is not None:

        processed_records.append(pd.DataFrame.from_dict(record, orient = 'index').T)

    bar.next()

records = pd.concat(processed_records)


# Assign who codes to the original WHO codes
records['original_who_code'] = records['who_code']

records = assign_id(records, min_id)

check_output(records)

# set date processed to NOW

log_records_per(records, 'dataset')
log_records_total(records)

records.to_csv('tmp/process/records.csv', index=False)

print('Success.')
logging.info("Success.")
