import pytest
import os
import shutil
import pandas as pd
from src.preprocess import utils


class Test_df_to_records:

    def test_is_list(self):
        '''test result is list'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        records = utils.df_to_records(df, 'ACAPS')

        assert type(records) == list

    def test_item_is_dict(self):
        '''test item is dict'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        records = utils.df_to_records(df, 'ACAPS')

        assert type(records[0]) == dict

    def test_item_dataset(self):
        '''test dataset key is dataset'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        dataset = 'ACAPS'

        records = utils.df_to_records(df, dataset)

        assert records[0]['dataset'] == dataset

    def test_raises_dataset_error(self):
        '''test that data with a "dataset" column with throw ValueError'''

        df = pd.DataFrame({'dataset': [1, 2, 3]})

        dataset = 'ACAPS'

        with pytest.raises(ValueError):
            utils.df_to_records(df, dataset)


class Test_split_df_by_group:

    def split_df_by_group_keys(self):

        data = pd.DataFrame({
            'a': ['a', 'b', 'c'],
            'b': [1, 2, 3],
        })

        res = utils.split_df_by_group(data, ['a'])

        assert all(x in ['a', 'b', 'c'] for x in res.keys())

    def split_df_by_group_values(self):

        data = pd.DataFrame({
            'a': ['a', 'b', 'c'],
            'b': [1, 2, 3],
        })

        res = utils.split_df_by_group(data, ['a'])

        assert all(x is pd.DataFrame for x in res.values())


class Test_remove_processed_records:

    def remove_processed_records_output_len(self):

        curr = pd.DataFrame({'id': [1, 2, 3, 4], 'value': [1, 2, 3, 4]})

        prev = pd.DataFrame({'id': [1, 2], 'value': [1, 2]})

        res = utils.remove_processed_records(curr, prev, 'id', 'id')

        assert len(res.index) == 3


# test get_row_hashes


def test_get_row_hashes_df():

    data = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 2, 1]})

    res = utils.get_row_hashes(data)

    assert type(res) is list


def test_get_row_hashes_len():

    data = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 2, 1]})

    res = utils.get_row_hashes(data)

    assert len(res) == 3


def test_get_row_hashes_bytes():

    data = pd.DataFrame({'a': [1, 2, 3], 'b': [3, 2, 1]})

    res = utils.get_row_hashes(data)

    assert type(res[0]) is bytes
