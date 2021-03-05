import pandas as pd
from src.postprocess import EURO


class Test_weekly_import:
    '''Test that the function correctly retrieve the specified weekly who_code'''

    def test_weekly_import(self):

        data = pd.DataFrame({
            'who_code': ['3.1.2', '1.4', '14', '4.1.2'],
            'dataset': ['EURO', 'EURO', 'EURO', 'EURO'],
            'importing': ['yes', 'no', 'yes', 'no']
        })
        
        who_code = pd.DataFrame({
        'who_code':['3.1.2','14']})

        res = EURO.weekly_import(data,who_code)
        
        expected_import = set(['3.1.2', '14'])
        
        assert len(set(list(res['who_code'])).difference(expected_import)) == 0
