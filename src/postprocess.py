"""
postprocess.py
====================================
Script to make manual changes to multiple dataset records.
"""

import pickle
import sys
import pandas as pd
import logging

from utils import create_dir
from postprocess.main import postprocess
from check import check_output

argv = sys.argv

create_dir('tmp/postprocess')

logging.basicConfig(filename='tmp/postprocess/postprocess.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

records = pd.read_csv('tmp/process/records.csv')

print("Postprocessing Data...")
logging.info("Postprocessing Data...")

records = records.groupby('dataset')
records = [records.get_group(x) for x in records.groups]

postprocessed = []

for data in records:

    postprocessed.append(postprocess(data))

records = pd.concat(postprocessed)

check_output(records)

print("Success.")
logging.info("Success.")
