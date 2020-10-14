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


class Test_admin_level_replacement:

    def test_null_admin_level(self):

        record = {'admin_level': ''}

        record = JH_HIT.null_admin_level(record, 'unknown')

        assert record['admin_level'] == 'unknown'

    def test_fill_admin_level_national(self):

        record = {'admin_level': 'Yes'}

        record = JH_HIT.fill_admin_level(record)

        assert record['admin_level'] == 'national'

    def test_fill_admin_level_state(self):

        record = {'admin_level': 'No'}

        record = JH_HIT.fill_admin_level(record)

        assert record['admin_level'] == 'state'


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


def test_replace_non_compliance_penalty():

    record = {'non_compliance_penalty': 'unknown'}

    record = JH_HIT.replace_non_compliance_penalty(record)

    assert record['non_compliance_penalty'] == 'Not Known'
