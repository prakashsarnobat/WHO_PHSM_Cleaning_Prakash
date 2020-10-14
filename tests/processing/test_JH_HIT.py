import pandas as pd
from src.processing import JH_HIT

class Test_apply_prov_measure_filter:

    def test_apply_prov_measure_filter_present(self):

        record = {'prov_category': 'a',
                  'prov_measure': 'b'}

        prov_measure_filter = pd.DataFrame({'prov_category': ['a'],
                                            'prov_measure': ['b']})

        record = JH_HIT.apply_prov_measure_filter(record, prov_measure_filter)

        assert type(record) == dict

    def test_apply_prov_measure_filter_absent(self):

        record = {'prov_category': 'c',
                  'prov_measure': 'd'}

        prov_measure_filter = pd.DataFrame({'prov_category': ['a'],
                                            'prov_measure': ['b']})

        record = JH_HIT.apply_prov_measure_filter(record, prov_measure_filter)

        assert record is None
