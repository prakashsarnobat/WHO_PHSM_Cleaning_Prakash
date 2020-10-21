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
from processing.utils import generate_blank_record
from utils import create_dir
from processing import check

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
           'ACAPS': pd.read_csv('config/key_map/ACAPS.csv').to_dict(orient='records')}

# load who country name reference
country_ref = pd.read_csv('config/country_names/who_country_names.csv')

#load who dataset coding
who_coding = {'JH_HIT': pd.read_csv('config/who_coding/JH_HIT.csv').fillna(''),
              'CDC_ITF': pd.read_csv('config/who_coding/CDC_ITF.csv').fillna(''),
              'ACAPS': pd.read_csv('config/who_coding/ACAPS.csv').fillna('')}

prov_measure_filter = {'JH_HIT': pd.read_csv('config/prov_measure_filter/JH_HIT.csv')}

blank_record = generate_blank_record()

processed_records = []

bar = Bar('Processing Data...', max=len(records))
for record in records:

    record = process(record, key_ref, country_ref, who_coding, prov_measure_filter)

    check.check_record_keys_agree(record, blank_record)

    if record is not None:

        processed_records.append(pd.DataFrame.from_dict(record, orient = 'index').T)

    bar.next()

#need checks of missing prov_ids and other issues - these hsould also work for mistress

records = pd.concat(processed_records)

records.to_csv('tmp/process/records.csv', index=False)
print('Success.')
logging.info("Success.")
