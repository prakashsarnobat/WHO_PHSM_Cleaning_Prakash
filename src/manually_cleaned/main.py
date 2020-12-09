"""
Main.py
====================================
Apply changes to manually cleaned data.

* If a record has a following_measure_number, update date_end and reason_ended values from the following record

* If measure stage is "finish", date_end should == date_start and reason_ended == 'finish'
"""

import pandas as pd

def adjust_manually_cleaned(manually_cleaned):

    #manually_cleaned = update_following_measures(manually_cleaned)

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

        if len(new_date_end) > 0:

            row['date_end'] = new_date_end
            row['reason_ended'] = new_reason_ended

        else:

            row['date_end'] = row['date_end']
            row['reason_ended'] = row['reason_ended']

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


def columns_to_lower(manually_cleaned: pd.DataFrame, lowercase_columns: list):
    '''Function to set all columns to lowercase'''

    for col in lowercase_columns:

        try:

            assert all(isinstance(x, str) for x in manually_cleaned[col] if not pd.isna(x))

        except AssertionError:

            raise AssertionError('Column {} does not only contain strings'.format(col))

        manually_cleaned[col] = manually_cleaned[col].str.lower()

    return(manually_cleaned)
