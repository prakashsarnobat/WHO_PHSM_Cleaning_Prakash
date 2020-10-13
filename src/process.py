"""
process.py
====================================
Script to apply dataset-specific transformers to individual dataset records.
"""

import pickle
import sys
import pandas as pd

from processing.main import process

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

for record in records:

    record = process(record, key_ref, country_ref, who_coding)
