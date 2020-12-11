import pandas as pd


def get_new_records(records: pd.DataFrame, previous_update: pd.DataFrame, cols: list):
    """
    Identify new records in an update data and a previous update data.

    Based on a string of `cols` pasted together to form an identifier.

    Example:

        Given `cols` = `['country_territory_area', 'date_start']`, pastes values in these columns together. Referred to as a "combo string".

        Any records in `records` with a "combo string" in `previous_update` will be not be recognised as a new record.

        i.e. "United States of America_2020-01-01" == "United States of America_2020-01-01" means that records match.

    Parameters
    ----------
    records : pd.DataFrame
        Newly updated data.
    previous_update : pd.DataFrame
        Previously updated data.
    cols : list
        Columns to be considered when merging records.

    Returns
    -------
    pd.DataFrame
        New records not present in `previous_update`.

    """

    records = records.copy()

    previous_update = previous_update.copy()

    # Concatenate values in `cols` separated by "_" in update data
    records['combo_string'] = get_combo_string(records, cols)

    # And previous update
    previous_update['combo_string'] = get_combo_string(previous_update, cols)

    # Identify which concatenated strings are unique in the new data
    new_combo_strings = set(records['combo_string']).difference(set(previous_update['combo_string']))

    #print(len(records['combo_string']))
    #print(len(new_combo_strings))
    #print(list(new_combo_strings)[0])
    #print(records.loc[records['combo_string'] == list(new_combo_strings)[0], 'comments'])

    # get a subset of the update data by these unique strings
    new_records = records.loc[[x in new_combo_strings for x in records['combo_string']], :]

    new_records = new_records.drop(['combo_string'], axis=1)

    return(new_records)


def get_combo_string(records, cols):

    combo_string = records[cols].apply(lambda x: x.astype(str)).agg('_'.join, axis=1)

    return(combo_string)
