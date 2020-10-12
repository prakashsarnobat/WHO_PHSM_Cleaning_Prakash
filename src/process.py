"""
process.py
====================================
Script to apply dataset-specific transformers to individual dataset records.
"""

import pickle
import sys

from processing.main import process

argv = sys.argv

fn = "tmp/preprocess/records.pickle"

records = pickle.load(open(fn, "rb"))

for record in records:

    record = process(record)
