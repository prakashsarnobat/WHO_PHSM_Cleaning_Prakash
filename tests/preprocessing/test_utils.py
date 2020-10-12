import pytest
import os
import shutil
import pandas as pd
from src.preprocess.utils import df_to_records, create_tmp


class Test_df_to_records:

    def test_is_list(self):
        '''test result is list'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        records = df_to_records(df, 'ACAPS')

        assert type(records) == list

    def test_item_is_dict(self):
        '''test item is dict'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        records = df_to_records(df, 'ACAPS')

        assert type(records[0]) == dict

    def test_item_dataset(self):
        '''test dataset key is dataset'''

        df = pd.DataFrame({'a': [1, 2, 3]})

        dataset = 'ACAPS'

        records = df_to_records(df, dataset)

        assert records[0]['dataset'] == dataset

    def test_raises_dataset_error(self):
        '''test that data with a "dataset" column with throw ValueError'''

        df = pd.DataFrame({'dataset': [1, 2, 3]})

        dataset = 'ACAPS'

        with pytest.raises(ValueError):
            df_to_records(df, dataset)


class Test_create_tmp:

    def test_dir_created(self):
        '''test that a tmp dir is created'''

        create_tmp()

        assert os.path.exists('tmp')

        shutil.rmtree('tmp')

    def test_dir_replaced(self):
        '''test that a tmp dir is replaced if it exists'''

        os.mkdir('tmp')
        os.mkdir('tmp/misc')

        assert os.path.exists('tmp/misc')

        create_tmp()

        assert not os.path.exists('tmp/misc')

        shutil.rmtree('tmp')
