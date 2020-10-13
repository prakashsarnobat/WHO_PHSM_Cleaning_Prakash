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
key_ref = pd.read_csv('config/key_map/JH_HIT.csv')
key_ref = key_ref.to_dict(orient='records')

# load who country name reference
country_ref = pd.read_csv('config/country_names/who_country_names.csv')

#load who dataset coding
who_coding = pd.read_csv('config/who_coding/JH_HIT.csv')
who_coding = who_coding.fillna('')

blank_record = generate_blank_record()

for record in records:

    record = process(record, key_ref, country_ref, who_coding)

    try:
        assert set(blank_record.keys()) == set(record.keys())

    except Exception as e:

        #replace with Logging
        print('Record keys do not agree.')
        print('Keys missing in Record: ' + ', '.join(str(x) for x in set(blank_record.keys()).difference(set(record.keys()))))
        print('Keys present in Record: ' + ', '.join(str(x) for x in set(record.keys()).difference(set(blank_record.keys()))))

        raise e
