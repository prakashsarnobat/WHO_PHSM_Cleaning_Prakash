"""
process.py
====================================
Script to apply dataset-specific transformers to individual dataset records.
"""

import pickle
import sys
import pandas as pd

from processing.main import process
from processing.utils import generate_blank_record

argv = sys.argv

fn = "tmp/preprocess/records.pickle"

records = pickle.load(open(fn, "rb"))

# load key transformation reference
key_ref = {'JH_HIT': pd.read_csv('config/key_map/JH_HIT.csv').to_dict(orient='records'),
           'CDC_ITF': pd.read_csv('config/key_map/CDC_ITF.csv').to_dict(orient='records')}

# load who country name reference
country_ref = pd.read_csv('config/country_names/who_country_names.csv')

#load who dataset coding
who_coding = {'JH_HIT': pd.read_csv('config/who_coding/JH_HIT.csv').fillna(''),
              'CDC_ITF': pd.read_csv('config/who_coding/CDC_ITF.csv').fillna('')}

prov_measure_filter = {'JH_HIT': pd.read_csv('config/prov_measure_filter/JH_HIT.csv')}

blank_record = generate_blank_record()

processed_records = []

for record in records:

    record = process(record, key_ref, country_ref, who_coding, prov_measure_filter)

    if not record is None:

        try:

            assert set(blank_record.keys()) == set(record.keys())

        except Exception as e:

            #replace with Logging
            print('Record keys do not agree.')
            print('Keys missing in Record: ' + ', '.join(str(x) for x in set(blank_record.keys()).difference(set(record.keys()))))
            print('Keys present in Record: ' + ', '.join(str(x) for x in set(record.keys()).difference(set(blank_record.keys()))))

            raise e

    processed_records.append(record)

#print([x for x in processed_records if x is not None])
