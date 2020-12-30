import pandas as pd
from progress.bar import Bar

def adjust_manually_cleaned(manually_cleaned: pd.DataFrame):
    """
    Unify value adjustments in manually cleaned data.

    Parameters
    ----------
    manually_cleaned : pd.DataFrame
        Manually cleaned data.

    Returns
    -------
    pd.DataFrame
        Description of returned object.

    """

    manually_cleaned = update_measure_stage_date(manually_cleaned)

    manually_cleaned = update_following_measures(manually_cleaned)

    return(manually_cleaned)


def update_following_measures(manually_cleaned: pd.DataFrame):
    """

    Update `date_end` values for records that have been assigned a following record.

    Parameters
    ----------
    manually_cleaned : pd.DataFrame
        Manually cleaned data.

    Returns
    -------
    pd.DataFrame
        Manually cleaned data with `date_end` values adjusted.

    """

    # Identify records with a following_measure_number
    has_following_measure = pd.Series([not pd.isna(x) for x in manually_cleaned['following_measure_number']])

    # Filter dataset by records with following_measure_number
    to_alter = manually_cleaned[has_following_measure]

    # Filter dataset by records with no following_measure_number
    not_to_alter = manually_cleaned[~has_following_measure]

    to_alter_res = []

    to_alter = [x for x in to_alter.iterrows()]

    bar = Bar('Processing Data...', max=len(to_alter))

    for i, row in to_alter:

        following_measure_number = row['following_measure_number']

        following_measure = manually_cleaned.loc[manually_cleaned['who_id'] == following_measure_number, :]

        try:

            new_date_end = list(following_measure['date_start'])[0]

        except Exception:

            new_date_end = None

        try:

            new_reason_ended = list(following_measure['measure_stage'])[0]

        except Exception:

            new_reason_ended = None

        if not pd.isna(new_date_end):

            row['date_end'] = new_date_end
            row['reason_ended'] = new_reason_ended

        else:

            row['date_end'] = row['date_end']
            row['reason_ended'] = row['reason_ended']

        to_alter_res.append(row)

        bar.next()

    bar.finish()

    to_alter = pd.DataFrame(to_alter_res)

    assert (len(to_alter.index) + len(not_to_alter.index)) == len(manually_cleaned.index)

    return(pd.concat([to_alter, not_to_alter]))


def update_measure_stage_date(manually_cleaned: pd.DataFrame):
    """

    Updates `date_end` and `reason_ended` based on `measure_stage` value.

    If measure stage is "finish", date_end should == date_start and reason_ended == "finish".

    Parameters
    ----------
    manually_cleaned : pd.DataFrame
        Manually cleaned data.

    Returns
    -------
    pd.DataFrame
        Manually cleaned data with adjustments.

    """

    is_null_date_end = pd.isna(manually_cleaned['date_end'])
    is_finish = manually_cleaned['measure_stage'] == 'finish'

    manually_cleaned.loc[(is_null_date_end) & (is_finish), "reason_ended"] = 'finish'
    manually_cleaned.loc[(is_null_date_end) & (is_finish), "date_end"] = manually_cleaned.loc[(is_null_date_end) & (is_finish), "date_start"]

    return(manually_cleaned)


def columns_to_lower(manually_cleaned: pd.DataFrame, lowercase_columns: list):
    """
    Set all values in a column to lowercase.

    Parameters
    ----------
    manually_cleaned : pd.DataFrame
        Manually cleaned data.
    lowercase_columns : list
        list of columns to transform to lowercase.

    Returns
    -------
    pd.DataFrame
        Manually cleaned data with conversion applied.

    """

    for col in lowercase_columns:

        try:

            assert all([isinstance(x, str) for x in manually_cleaned[col] if not pd.isna(x)])

        except AssertionError:

            raise AssertionError('Column {} does not only contain strings'.format(col))

        manually_cleaned[col] = manually_cleaned[col].str.lower()

    return(manually_cleaned)
