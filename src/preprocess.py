"""
preprocess.py
====================================
Script to convert provider datasets to standard column names and apply column formatting
"""

import json

import pandas as pd

from preprocess.column_map import apply_column_map

# Source of config file - also move to Makefile when ready
column_map = "config/column_map.json"

# Dataset sources: these should be in makefile when ready
jh = "https://raw.githubusercontent.com/HopkinsIDD/hit-covid/master/data/hit-covid-longdata.csv"

# replace this with logging
print("Reading column map")
with open(column_map) as json_file:
    column_map = json.load(json_file)

# replace this with logging
print("Reading JH")
jh = pd.read_csv(jh).to_dict(orient='records')

print(jh)

exit()

jh = apply_column_map(jh, "JH_HIT", column_map)

print(jh.columns)
