import pytest
import pandas as pd
from src import check

class Test_check_duplicate_id:

    def test_check_duplicate_id_correct(self):
        '''Test that nothing happens if there are no duplicates'''

        data = pd.DataFrame({'who_id':[1, 2, 3]})
        key = 'who_id'

        res = check.check_duplicate_id(data, key, log=False)

        assert res is None

    def test_check_duplicate_id_errors(self):
        '''Test that error is thrown if there are duplicates'''

        data = pd.DataFrame({'who_id':[1, 1, 3]})
        key = 'who_id'

        with pytest.raises(AssertionError):

            check.check_duplicate_id(data, key, log=False)
