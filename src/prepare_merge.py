'''
prepare_merge.py

Script to merge prop IDs from previous weeks with not_cleansed data to detect changes

#NOTE - currently under development, not used in production 2020-12-09

'''
import pandas as pd
from datetime import datetime

merge_columns = ["prop_id",
                 "country_territory_area",
                 "dataset",
                 "area_covered",
                 "who_code",
                 "date_start"]

previous_update = pd.read_csv('data/merge/update_merge_2020_11_25.csv')

previous_not_cleansed = pd.read_csv('data/not_cleansed/master_2020_12_02.csv')


def combine_updates(previous_update, previous_not_cleansed, merge_columns):
    '''Function to combine information from previous not_cleansed data'''

    previous_not_cleansed = previous_not_cleansed.loc[previous_not_cleansed['processed'] == 'not_cleansed', :]

    previous_not_cleansed = previous_not_cleansed[merge_columns]

    return(previous_not_cleansed)

update_merge = combine_updates(previous_update, previous_not_cleansed, merge_columns)

update_merge.to_csv('data/merge/update_merge_{}.csv'.format(datetime.now().strftime('%Y_%m_%d')))
