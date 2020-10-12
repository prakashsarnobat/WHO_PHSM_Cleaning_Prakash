# Should have separate section that checks that config files are ok before passing them here


def apply_column_map(data, dataset, col_map):
    """ function to apply column_map to all columns in a dataset"""

    col_map = col_map["data"][dataset]

    for cm in col_map:

        data = column_map(data, cm["orig_col"], cm["new_col"])

    # drop columns named with empty strings (the null value in config/column_map.json)
    data.drop([""], axis=1, inplace=True)

    return data


def column_map(data, orig_name, new_name):
    """function to map column names from provider names to who names"""

    data.rename(columns={orig_name: new_name}, inplace=True)

    return data
