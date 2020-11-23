import os
import pickle
import shutil
import re

from pandas import DataFrame


def df_to_records(df: DataFrame, dataset: str, drop_columns = []):
    """Function to convert dataframe to record oriented - dict"""

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

    try:

        print("Writing records.pickle...")

        pickle.dump(records, open(dir + "/" + "records.pickle", "wb"))

    except Exception as e:

        shutil.rmtree(dir)

        raise e("Unable to write tmp/preprocess/records.p.")


def oxcgrt_records(ox, dataset, drop_columns=[]):
    '''
    Function to convert OXCGRT data to records

    This is an additional challenge because of the wide format of the Oxford data
    '''

    full_value_names, value_names, stub_names = get_names(ox)

    id_columns = [x for x in list(set(ox.columns).difference(set(full_value_names))) if x not in drop_columns]

    records = ox.to_dict(orient="records")

    rs = [x for x in [get_measure_records(r, stub_names, id_columns, full_value_names) for r in records] if x != []]

    rs = [item for sublist in rs for item in sublist]

    return(rs)


def get_names(ox):
    '''
    Function to get names of columns holding measure information.

    These columns begin with the prefix "A1\_" etc.

    returns:
        full_value_names: the names of all columns with measure information
        value_names: the names of measure columns
        stub_names: the measure column prefixes (i.e. "A1")

    '''

    stub_exp = r'[A-Z][0-9]+_'

    full_value_names = [match for match in ox.columns if re.findall(stub_exp , match) != []]

    value_names = [x for x in full_value_names if 'Flag' not in x]
    value_names = [x for x in value_names if 'Notes' not in x]

    stub_names = [x.split('_')[0] for x in value_names]

    return(full_value_names, value_names, stub_names)


def get_measure_records(combined_record, stub_names, id_columns, full_value_names):
    '''Function to break rows into individual records by stub group

        i.e. subset a row for only C4 records and other information, repeat for all possible measures.

        Also drops records where notes column is blank i.e. sum(notes columns) == 0

    '''

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
