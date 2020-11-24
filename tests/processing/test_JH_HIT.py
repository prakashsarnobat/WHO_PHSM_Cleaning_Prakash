import numpy as np
import pandas as pd
from src.processing import JH_HIT


class Test_blank_record_and_url:

    def test_blank_record_and_url_none(self):
        '''
        Test that blank records are labelled when missing values are None
        '''

        record = {'comments': None,
                  'link': None,
                  'alt_link': None,
                  'who_code': None,
                  'who_category': None,
                  'who_subcategory': None,
                  'who_measure': None}

        res = JH_HIT.blank_record_and_url(record)

        assert res['who_code'] == '11'
        assert res['who_category'] == 'Not enough to code'
        assert res['who_subcategory'] == 'Not enough to code'
        assert res['who_measure'] == 'Not enough to code'

    def test_blank_record_and_url_nan(self):
        '''
        Test that blank records are labelled when missing values are np.nan
        '''

        record = {'comments': np.nan,
                  'link': np.nan,
                  'alt_link': np.nan,
                  'who_code': None,
                  'who_category': None,
                  'who_subcategory': None,
                  'who_measure': None}

        res = JH_HIT.blank_record_and_url(record)

        assert res['who_code'] == '11'
        assert res['who_category'] == 'Not enough to code'
        assert res['who_subcategory'] == 'Not enough to code'
        assert res['who_measure'] == 'Not enough to code'

    def test_blank_record_and_url_filled(self):
        '''
        Test that records are not labelled when at least one field is filled in
        '''

        record = {'comments': 'anything',
                  'link': None,
                  'alt_link': None,
                  'who_code': None,
                  'who_category': None,
                  'who_subcategory': None,
                  'who_measure': None}

        res = JH_HIT.blank_record_and_url(record)

        assert res['who_code'] is None
        assert res['who_category'] is None
        assert res['who_subcategory'] is None
        assert res['who_measure'] is None


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
