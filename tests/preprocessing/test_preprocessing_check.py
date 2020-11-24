import pytest
import pandas as pd
from src.preprocess import check

class Test_check_column_names:

    def test_check_column_names(self):

        records = pd.DataFrame({'a': [1]})
        config = pd.DataFrame({'column': ['a'], 'dataset': ['ACAPS']})

        res = check.check_column_names(records, config, log=False)

        assert res is None
