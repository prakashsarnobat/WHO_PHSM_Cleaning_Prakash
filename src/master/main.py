import pandas as pd

def get_new_records(records: pd.DataFrame, manually_cleaned, cols):
    ''' This needs to be replaced with an interfeace between old_ids and new_ids'''

    records['combo_string'] = get_combo_string(records, cols)
    manually_cleaned['combo_string'] = get_combo_string(manually_cleaned, cols)

    new_combo_strings = set(records['combo_string']).difference(set(manually_cleaned['combo_string']))

    new_records = records.loc[[x in new_combo_strings for x in records['combo_string']], :]

    return(new_records)


def get_combo_string(records, cols):

    combo_string = records[cols].apply(lambda x: x.astype(str)).agg('_'.join, axis=1)

    return(combo_string)
