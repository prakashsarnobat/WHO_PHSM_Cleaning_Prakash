import pickle
import shutil
import re
import hashlib
import base64
from datetime import datetime

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
        except Exception:
            pass

        try:
            notes_key = [x for x in stub_keys if '_Notes' in x][0]
        except Exception:
            pass

        subset = {key: value for key, value in combined_record.items() if key in keys}

        # Pass record if notes are blank
        try:
            if sum([subset[notes_key]]) == 0:

                continue
        except Exception:
            pass

        try:
            subset['flag'] = subset.pop(flag_key)
        except Exception:
            subset['flag'] = 0.0
            pass

        try:
            subset['notes'] = subset.pop(notes_key)
        except Exception:
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


def filter_new_hashes(data: pd.DataFrame,
                      ingested_path: str,
                      date_now: str = datetime.now().strftime('%Y_%m_%d')) -> pd.DataFrame:
    """
    Filter records by the row-wise hashes of their content.

    Reduces the number of records that need to be processed from each dataset.

    Will not filter hashes that were ingested on the same day as the function is called.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    ingested_path : str
        Path to ingested hash reference.
    date_now : str
        String of current date.

    Returns
    -------
    pd.DataFrame
        Filtered data.

    """

    # Read the reference file for ingested hashes
    ingested_hash_ref = pd.read_csv(ingested_path)

    # Filter for hashes that were not processed today
    ingested_hash_ref.loc[ingested_hash_ref['date_processed'] != date_now, :]

    # Define row-wise hashes for the input dataset
    data['_hash'] = get_row_hashes(data)

    # Filter for only hash values that have not been processed on a different day
    data = data.loc[[x not in ingested_hash_ref['hash'] for x in data['_hash']]]

    # Get the hashes that were just ingested
    new_hashes = pd.DataFrame({'hash': data['_hash'], 'date_processed': date_now})

    # Remove _hash column from new data
    data = data.drop(columns=['_hash'])

    # Combine previous hash ref with new hash ref
    ingested_hash_ref = pd.concat([ingested_hash_ref, new_hashes]).drop_duplicates()

    # Write combined hash ref to csv file
    ingested_hash_ref.to_csv(ingested_path, index=False)

    return(data)


def get_row_hashes(data: pd.DataFrame) -> list:
    """
    Get row-wise base64 encoded hashes for a dataframe.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.

    Returns
    -------
    list
        list of hashes.

    """

    # Combine row values into a single string
    hash_strings = list(data.apply(lambda x: ''.join([str(x) for x in tuple(x)]), axis = 1))

    # Hash and base64 encode string
    hashes = [base64.b64encode(hashlib.sha1(x.encode("UTF-8")).digest()) for x in hash_strings]

    return(hashes)
