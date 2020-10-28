"""
Main.py
====================================
Apply changes to manually cleaned data.

* If a record has a following_measure_number, update date_end and reason_ended values from the following record

* If measure stage is "finish", date_end should == date_start and reason_ended == 'finish'
"""

import pandas as pd

def adjust_manually_cleaned(manually_cleaned):

    manually_cleaned = update_following_measures(manually_cleaned)

    manually_cleaned = update_measure_stage_date(manually_cleaned)

    return(manually_cleaned)

def update_following_measures(manually_cleaned):

    has_following_measure = pd.Series([not pd.isna(x) for x in manually_cleaned['following_measure_number']])

    to_alter = manually_cleaned[has_following_measure]

    not_to_alter = manually_cleaned[~has_following_measure]

    to_alter_res = []

    for i, row in to_alter.iterrows():

        following_measure_number = row['following_measure_number']

        following_measure = manually_cleaned.loc[manually_cleaned['who_id'] == following_measure_number, :]

        new_date_end = following_measure['date_start']

        new_reason_ended = following_measure['measure_stage']

        row['date_end'] = new_date_end
        row['reason_ended'] = new_reason_ended

        to_alter_res.append(row)

    to_alter = pd.concat([x.to_frame().T for x in to_alter_res])

    assert (len(to_alter.index) + len(not_to_alter.index)) == len(manually_cleaned.index)

    return(pd.concat([to_alter, not_to_alter]))


def update_measure_stage_date(manually_cleaned):
    '''* If measure stage is "finish", date_end should == date_start and reason_ended == 'finish'''

    is_null_date_end = pd.isna(manually_cleaned['date_end'])
    is_finish = manually_cleaned['measure_stage'] == 'finish'

    manually_cleaned.loc[(is_null_date_end) & (is_finish), "reason_ended"] = 'finish'
    manually_cleaned.loc[(is_null_date_end) & (is_finish), "date_end"] = manually_cleaned.loc[(is_null_date_end) & (is_finish), "date_start"]

    return(manually_cleaned)
