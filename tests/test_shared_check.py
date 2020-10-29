import pytest
import pandas as pd
from src import check

class Test_check_duplicate_id:

    def test_check_duplicate_id_correct(self):
        '''Test that nothing happens if there are no duplicates'''

        data = pd.DataFrame({'who_id':[1, 2, 3]})
        key = 'who_id'

        res = check.check_duplicate_id(data, key, log=False)

        assert res

    def test_check_duplicate_id_dup(self):
        '''Test that False is returned if there are duplicates'''

        data = pd.DataFrame({'who_id':[1, 1, 3]})
        key = 'who_id'

        res = check.check_duplicate_id(data, key, log=False)

        assert not res

class Test_check_values_present():

    def test_check_values_present(self):
        '''Test that values in one column are present in another column'''

        data = pd.DataFrame({'focus_col':[1, None, 2], 'ref_col':[1, 2, 3]})

        res = check.check_values_present(data, 'focus_col', 'ref_col', log=False)

        assert res

    def test_check_values_present_missing(self):
        '''Test that check is false if values in one column are not present in another column'''

        data = pd.DataFrame({'focus_col':[1, 500, 2], 'ref_col':[1, 2, 3]})

        res = check.check_values_present(data, 'focus_col', 'ref_col', log=False)

        assert not res
