import os
import pickle
import shutil

from pandas import DataFrame


def df_to_records(df: DataFrame, dataset: str):
    """Function to convert dataframe to record oriented - dict"""

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


def create_tmp():
    """Function to create or replace a "tmp" directory"""
    dir = "tmp"

    if os.path.exists(dir):

        shutil.rmtree(dir)

    os.mkdir(dir)

def write_records(records: list, subdir: str, fn: str):

    try:
        create_tmp()
        os.mkdir("tmp" + "/" + subdir)

        print("Writing records.pickle...")

        pickle.dump(records, open("tmp" + "/" + subdir + "/" + "records.pickle", "wb"))

    except Exception as e:

        shutil.rmtree("tmp")

        raise e("Unable to write tmp/preprocess/records.p.")
