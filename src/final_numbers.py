"""
Script to output the final numbers for checking between master and mistress files
"""

import pandas as pd

master = pd.read_csv('data/not_cleansed/master_latest.csv',
                     low_memory=False)

nums = {}

nums['num_total'] = len(master.index)
nums['num_seq'] = len(master.loc[master['processed'] == 'sequenced'].index)
nums['num_not_cleansed'] = len(master.loc[master['processed'] == 'not_cleansed'].index)
nums['num_keep_n'] = len(master.loc[master['keep'] == 'n'].index)
nums['num_keep_y_seq'] = len(master.loc[(master['processed'] == 'sequenced') & (master['keep'] == 'y')].index)

print('Summary numbers for final checks...')
print('Total Number: {}'.format(nums['num_total']))
print('Number Sequenced: {}'.format(nums['num_seq']))
print('Number New: {}'.format(nums['num_not_cleansed']))
print('Number Not of interest: {}'.format(nums['num_keep_n']))
print('Unique Records: {}'.format(nums['num_keep_y_seq']))
print('Done! \U0001F389')
