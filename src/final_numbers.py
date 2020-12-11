"""
final_numbers.py

Script to output the final numbers for checking between master and mistress files
"""

import pandas as pd

# Read most recent master dataset
master = pd.read_csv('data/not_cleansed/master_latest.csv',
                     low_memory=False)

# Dict to store record numbers from checks
nums = {}

# Get total number of record
nums['num_total'] = len(master.index)

# Get number of sequenced records
nums['num_seq'] = len(master.loc[master['processed'] == 'sequenced'].index)

# Get number of not_cleansed records
nums['num_not_cleansed'] = len(master.loc[master['processed'] == 'not_cleansed'].index)

# Get number of records where keep == 'n'
nums['num_keep_n'] = len(master.loc[master['keep'] == 'n'].index)

# Get number or records that will be included in the release (keep == 'y' and processed == 'sequenced')
nums['num_keep_y_seq'] = len(master.loc[(master['processed'] == 'sequenced') & (master['keep'] == 'y')].index)

# Print final numbers to console
print('Summary numbers for final checks...')
print('Total Number: {}'.format(nums['num_total']))
print('Number Sequenced: {}'.format(nums['num_seq']))
print('Number New: {}'.format(nums['num_not_cleansed']))
print('Number Not of interest: {}'.format(nums['num_keep_n']))
print('Unique Records: {}'.format(nums['num_keep_y_seq']))
print('Done! \U0001F389')
