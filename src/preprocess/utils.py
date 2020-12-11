import os
import pickle
import shutil
import re

import pandas as pd


def df_to_records(df: pd.DataFrame, dataset: str, drop_columns = []):
    """
    Convert dataframe to a list of record oriented dicts.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    dataset : str
        Name of provider dataset.
    drop_columns : type
        Which columns (if any) to drop.

    Returns
    -------
    list
        List of row-wise dicts.

    """

    if dataset == 'OXCGRT':

        records = oxcgrt_records(df, dataset, drop_columns)

    else:

        records = df.to_dict(orient="records")

    # ensure that the dataset doesn't have a `dataset` column
    # if so, we will have to change this
    try:

        assert "dataset" not in records[0].keys()

    except Exception as e:
        raise ValueError('Input dataset contains "dataset" column name.')

    # assign a dataset key to each record
    for x in records:
        x["dataset"] = dataset

    return records


def write_records(records: list, dir: str, fn: str):
    """
    Write records to a pickle file.

    Parameters
    ----------
    records : list
        List of preprocessed records.
    dir : str
        Output directory.
    fn : str
        Output file name.

    Returns
    -------
    None

    """

    try:

        print("Writing records.pickle...")

        pickle.dump(records, open(dir + "/" + "records.pickle", "wb"))

    except Exception as e:

        shutil.rmtree(dir)

        raise e("Unable to write tmp/preprocess/records.p.")


def oxcgrt_records(ox: pd.DataFrame, dataset: str, drop_columns: list = []):
    """
    Function to convert OXCGRT data to list of record dicts.

    This presents an additional challenge because of the wide format of the OXCGRT data.

    Parameters
    ----------
    ox : pd.DataFrame
        Input OXCGRT data.
    dataset : str
        Name of provider dataset.
    drop_columns : list
        Which columns (if any) to drop.

    Returns
    -------
    list
        List of record dicts.

    """

    full_value_names, value_names, stub_names = get_names(ox)

    id_columns = [x for x in list(set(ox.columns).difference(set(full_value_names))) if x not in drop_columns]

    records = ox.to_dict(orient="records")

    rs = [x for x in [get_measure_records(r, stub_names, id_columns, full_value_names) for r in records] if x != []]

    rs = [item for sublist in rs for item in sublist]

    return(rs)


def get_names(ox: pd.DataFrame):
    """
    Get the names of columns holding measure information.

    These columns begin with the prefix "A1\_" etc.

    returns:
        full_value_names: the names of all columns with measure information
        value_names: the names of measure columns
        stub_names: the measure column prefixes (i.e. "A1")

    Parameters
    ----------
    ox : pd.DataFrame
        Input OXCGRT dataset.

    Returns
    -------
    full_value_names: list
        The names of all columns with measure information.
    value_names: list
        The names of measure columns.
    stub_names: list
        The measure column prefixes (i.e. "A1").

    """

    stub_exp = r'[A-Z][0-9]+_'

    full_value_names = [match for match in ox.columns if re.findall(stub_exp , match) != []]

    value_names = [x for x in full_value_names if 'Flag' not in x]
    value_names = [x for x in value_names if 'Notes' not in x]

    stub_names = [x.split('_')[0] for x in value_names]

    return(full_value_names, value_names, stub_names)


def get_measure_records(combined_record, stub_names, id_columns, full_value_names):
    """
    Function to break rows into individual records by stub group.

    i.e. subset a row for only C4 records and other information, repeat for all possible measures.

    Also drops records where notes column is blank i.e. sum(notes columns) == 0.

    Parameters
    ----------
    combined_record : type
        Dict of a single OXCGRT row.
    stub_names : type
        List of names of each stub group.
    id_columns : type
        List of columns to be retained as IDs.
    full_value_names : type
        List of full names of value columns.

    Returns
    -------
    list
        List of dicts containing all records extracted from a given row.

    """

    records = []

    for stub in stub_names:

        stub_keys = [x for x in full_value_names if stub in x]

        keys = id_columns + stub_keys

        try:
            flag_key = [x for x in stub_keys if '_Flag' in x][0]
        except:
            pass

        try:
            notes_key = [x for x in stub_keys if '_Notes' in x][0]
        except:
            pass

        subset = {key: value for key, value in combined_record.items() if key in keys}

        # Pass record if notes are blank
        try:
            if sum([subset[notes_key]]) == 0:

                continue
        except:
            pass

        try:
            subset['flag'] = subset.pop(flag_key)
        except:
            subset['flag'] = 0.0
            pass

        try:
            subset['notes'] = subset.pop(notes_key)
        except:
            pass


        #replace 0.0 in id columns with None
        for col in id_columns:

            if subset[col] == 0.0:

                subset[col] = None

        measure_key = list(set(list(subset.keys())).difference(set(id_columns + ['measure_name', 'flag', 'notes'])))

        subset['measure'] = subset.pop(measure_key[0])

        subset['measure_name'] = measure_key[0]

        records.append(subset)

    return(records)


def split_df_by_group(data: pd.DataFrame, group: str):
    """
    Split a dataframe by group and return a named dictionary.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset.
    group : str
        Name of column to be used as group.

    Returns
    -------
    dict
        Dict of dataset slices named by group.

    """

    grouped = data.groupby(group)

    groups = grouped.groups

    grouped = [grouped.get_group(x) for x in grouped.groups]

    return(dict(zip(groups, grouped)))


def remove_processed_records(dataset: pd.DataFrame,
                             previous_update: pd.DataFrame,
                             current_id_col_name: str,
                             prev_id_col_name: str = 'prop_id'):
    """
    Drop previously ingested records.

    Parameters
    ----------
    dataset : pd.DataFrame
        Input dataset.
    previous_update : pd.DataFrame
        Reference for previously ingested records.
    current_id_col_name : str
        Column name od ID values in current data.
    prev_id_col_name : str
        Column name od ID values in previously ingested data.

    Returns
    -------
    pd.DataFrame
        Dataframe with previously ingested records filtered out.

    """

    current_ids = dataset[current_id_col_name]

    prev_ids = previous_update[prev_id_col_name]

    new_ids = set(current_ids).difference(set(prev_ids))

    new_records = dataset.loc[[x in new_ids for x in dataset[current_id_col_name]], :]

    return(new_records)
