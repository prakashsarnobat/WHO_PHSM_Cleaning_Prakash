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


class Test_fill_not_enough_to_code:

    def test_fill_not_enough_to_code(self):

        record = {'comments': '',
                  'prov_measure': 'a',
                  'prov_category': 'a'}

        record = JH_HIT.fill_not_enough_to_code(record)

        assert record['prov_measure'] == 'not_enough_to_code'
        assert record['prov_category'] == 'not_enough_to_code'

    def test_fill_not_enough_to_code_school(self):

        record = {'comments': '',
                  'prov_measure': 'a',
                  'prov_category': 'school_closed'}

        record = JH_HIT.fill_not_enough_to_code(record)

        assert record['prov_measure'] == 'a'
        assert record['prov_category'] == 'school_closed'
