import pandas as pd
from src.postprocess import JH_HIT


class Test_combine_measures:
    '''Function to test that JH_HIT measures are combined correctly'''

    def test_combine_measures(self):

        data = pd.DataFrame({
            'uuid': [1, 2, 3, 4],
            'who_code': ['4.1.2', '4.1.2', '4.1.2', '10'],
            'who_id': ['A', 'B', 'C', 'D'],
            'targeted': ['primary', 'secondary', 'nursery', 'other'],
            'prop_id': ['1_school_primary', '1_school_primary', '1_school_primary', '4_other'],
            'dataset': ['JH_HIT'] * 4
        })

        res = JH_HIT.combine_measures(data, '4.1.2', '_school_closure', ['uuid', 'who_id', 'prop_id_numeric', 'who_code'])

        expected_codes = set(['4.1.2', '10'])
        expected_uuids = set([1, 4])
        expected_ids = set(['A', 'D'])
        expected_targeted = set(['primary, secondary, nursery', 'other'])

        assert len(res.index) == 2
        assert len(set(list(res['who_code'])).difference(expected_codes)) == 0
        assert len(set(list(res['uuid'])).difference(expected_uuids)) == 0
        assert len(set(list(res['who_id'])).difference(expected_ids)) == 0
        assert len(set(list(res['targeted'])).difference(expected_targeted)) == 0
