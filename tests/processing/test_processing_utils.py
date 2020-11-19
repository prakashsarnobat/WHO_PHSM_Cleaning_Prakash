import pytest

import pandas as pd
from src.processing.utils import generate_blank_record, key_map, apply_key_map, parse_date, assign_id, assign_who_country_name, assign_who_coding
from src.processing import utils

class Test_generate_blank_record:

    def test_is_dict(self):

        assert type(generate_blank_record()) == dict

    def test_dict_key_number(self):

        assert len(generate_blank_record().keys()) == 45


def test_create_id():

    id = utils.create_id('ACAPS', 6)

    assert len(id) == 12


class Test_new_id:

    def test_new_id(self):

        id = utils.new_id('ACAPS', 6)

        assert len(id) == 12

    def test_new_id_plausibly_unique(self):

        ids = []

        for i in range(0, 10000):

            ids.append(utils.new_id('ACAPS', existing_ids=ids))

        assert len(pd.unique(ids)) == len(ids)


class Test_key_map:

    def test_key_mapping(self):

        a = {'a': None}
        b = {'b': 'something'}

        a = key_map(a, b, 'a', 'b')

        assert a['a'] == 'something'

    def test_key_map_returns_dict(self):

        a = {'a': None}
        b = {'b': 'something'}

        a = key_map(a, b, 'a', 'b')

        assert type(a) == dict

    def test_key_map_missing_key(self):

        a = {'a': None}
        b = {'b': 'something'}

        with pytest.raises(KeyError):
            key_map(a, b, 'a', '')


class Test_apply_key_map:

    def test_key_mappings(self):

        a = {'a': None, 'b': None}
        b = {'c': 'something', 'd': 'something else'}

        key_map = [{'old_key': 'c', 'new_key': 'a'},
                    {'old_key': 'd', 'new_key': 'b'}
                    ]

        a = apply_key_map(a, b, key_map)

        assert a['a'] == 'something'
        assert a['b'] == 'something else'


class Test_parse_date:

    def test_parse_date_r_format(self):

        a = {'date_start': '2020-01-01', 'date_end': '2020-01-01', 'date_entry': '2020-01-01'}

        a = parse_date(a)

        assert type(a['date_start']) == pd.Timestamp

    def test_parse_date_usa_format(self):

        a = {'date_start': '04/30/2020', 'date_end': '04/30/2020', 'date_entry': '04/30/2020'}

        a = parse_date(a)

        assert type(a['date_start']) == pd.Timestamp

        assert a['date_start'].month == 4

    def test_parse_date_eu_format(self):

        a = {'date_start': '30/04/2020', 'date_end': '30/04/2020', 'date_entry': '30/04/2020'}

        a = parse_date(a)

        assert type(a['date_start']) == pd.Timestamp

        assert a['date_start'].month == 4

class Test_assign_id:

    def test_assign_id(self):

        a = pd.DataFrame({'dataset':['ACAPS'],
                          'a':['Anything']
         })

        a = assign_id(a, min_id=0)

        assert 'ACAPS_1' in list(a['who_id'])

class Test_assign_who_country_name:

    def test_assign_who_country_name(self):

        a = {'iso': 'AFG',
             'country_territory_area': 'Afghanistan'}

        country_ref = pd.DataFrame({'iso': ['AFG'],
                                    'who_region': ['REGION'],
                                    'country_territory_area': ['NAME'],
                                    'iso_3166_1_numeric': [1]})

        a = assign_who_country_name(a, country_ref)

        assert a['iso'] == 'AFG'

        assert a['who_region'] == 'REGION'

        assert a['country_territory_area'] == 'NAME'

        assert a['iso_3166_1_numeric'] == 1

    def test_assign_who_country_name_errors(self):

        a = {'iso': 'AFG',
             'country_territory_area': 'Afghanistan'}

        country_ref = pd.DataFrame({'iso': ['USA']})

        a = assign_who_country_name(a, country_ref)

        assert a['iso'] == 'AFG'

        assert a['who_region'] == 'unknown'

        assert a['country_territory_area'] == 'unknown'

        assert a['iso_3166_1_numeric'] == 'unknown'


class Test_assign_who_coding:

    def test_assign_who_coding(self):

        record = {}

        record['prov_measure'] = 'a'
        record['prov_subcategory'] = 'b'
        record['prov_category'] = 'c'

        who_coding = pd.DataFrame({'prov_measure': ['a'],
                                   'prov_subcategory': ['b'],
                                   'prov_category': ['c'],
                                   'who_code': [1],
                                   'who_measure': ['a'],
                                   'who_subcategory': ['b'],
                                   'who_category': ['c'],
                                   'non_compliance': ['d'],
                                   'who_targeted': ['e']})

        record = assign_who_coding(record, who_coding)

        assert record['who_code'] == 1

        assert record['who_measure'] == 'a'

        assert record['who_subcategory'] == 'b'

        assert record['who_category'] == 'c'

        assert record['non_compliance_penalty'] == 'd'

        assert record['targeted'] == 'e'

    def test_assign_who_coding_missing(self):

        record = {}

        record['dataset'] = 'ACAPS'
        record['prov_measure'] = 'a'
        record['prov_subcategory'] = 'b'
        record['prov_category'] = 'c'

        who_coding = pd.DataFrame({'prov_measure': ['b'],
                                   'prov_subcategory': ['b'],
                                   'prov_category': ['c'],
                                   'who_code': [1],
                                   'who_measure': ['a'],
                                   'who_subcategory': ['b'],
                                   'who_category': ['c']})

        record = assign_who_coding(record, who_coding)

        assert record['who_code'] == 'unknown'

        assert record['who_measure'] == 'unknown'

        assert record['who_subcategory'] == 'unknown'

        assert record['who_category'] == 'unknown'

    def test_assign_who_coding_duplicate(self):

        record = {}

        record['dataset'] = 'ACAPS'
        record['prov_measure'] = 'a'
        record['prov_subcategory'] = 'b'
        record['prov_category'] = 'c'

        who_coding = pd.DataFrame({'prov_measure': ['a', 'a'],
                                   'prov_subcategory': ['b', 'b'],
                                   'prov_category': ['c', 'c'],
                                   'who_code': [1, 1],
                                   'who_measure': ['a', 'a'],
                                   'who_subcategory': ['b', 'b'],
                                   'who_category': ['c', 'c']})

        record = assign_who_coding(record, who_coding)

        assert record['who_code'] == 'unknown'

        assert record['who_measure'] == 'unknown'

        assert record['who_subcategory'] == 'unknown'

        assert record['who_category'] == 'unknown'

    def test_assign_who_coding_targeted(self):

        record = {}

        record['prov_measure'] = 'a'
        record['prov_subcategory'] = 'b'
        record['prov_category'] = 'c'
        record['targeted'] = 'd'

        who_coding = pd.DataFrame({'prov_measure': ['a'],
                                   'prov_subcategory': ['b'],
                                   'prov_category': ['c'],
                                   'who_code': [1],
                                   'who_measure': ['a'],
                                   'who_subcategory': ['b'],
                                   'who_category': ['c'],
                                   'non_compliance': ['d'],
                                   'who_targeted': ['']})

        record = assign_who_coding(record, who_coding)

        assert record['targeted'] == 'd'

    def test_assign_who_coding_non_compliance(self):

        record = {}

        record['prov_measure'] = 'a'
        record['prov_subcategory'] = 'b'
        record['prov_category'] = 'c'
        record['non_compliance_penalty'] = 'f'

        who_coding = pd.DataFrame({'prov_measure': ['a'],
                                   'prov_subcategory': ['b'],
                                   'prov_category': ['c'],
                                   'who_code': [1],
                                   'who_measure': ['a'],
                                   'who_subcategory': ['b'],
                                   'who_category': ['c'],
                                   'non_compliance': [''],
                                   'who_targeted': ['a']})

        record = assign_who_coding(record, who_coding)

        assert record['non_compliance_penalty'] == 'f'


class Test_replace_conditional:

    def test_replace_conditional(self):

        record = {'anything': 'a'}

        record = utils.replace_conditional(record, 'anything', 'a', 'b')

        assert record['anything'] == 'b'


def test_shift_sensitive_region():

    record = record = {'country_territory_area': 'Kosovo'}

    record = utils.shift_sensitive_region(record, 'Kosovo', 'Serbia')

    assert record['country_territory_area'] == 'Serbia'

    assert record['area_covered'] == 'Kosovo'

class Test_add_admin_level:

    def test_add_admin_level_national(self):

        record = {'area_covered':None, 'admin_level': ''}

        record = utils.add_admin_level(record)

        assert record['admin_level'] == 'national'

    def test_add_admin_level_other(self):

        record = {'area_covered':'Anything', 'admin_level': ''}

        record = utils.add_admin_level(record)

        assert record['admin_level'] == 'other'

class Test_remove_tags:

    def test_remove_tags_text(self):
        '''test that plain text is left alone'''

        sent = 'A sentence'

        record = {'comments':sent}

        record = utils.remove_tags(record, ['comments'])

        assert record['comments'] == sent

    def test_remove_tags_li(self):
        '''test that html tags are removed'''

        sent = '<li>A sentence</li>'

        record = {'comments':sent}

        record = utils.remove_tags(record, ['comments'])

        assert record['comments'] == 'A sentence'

    def test_remove_tags_none(self):

        record = {'comments':None}

        record = utils.remove_tags(record, ['comments'])

        assert record['comments'] is None

    def test_remove_tags_misc(self):

        records = [{'comments':"Anything<p>"},
            {'comments':'Anything<a href="'},
            {'comments':'Anything/">'},
            {'comments':"Anything<p>"},
            {'comments':"Anything</a>"}]

        for record in records:

            record = utils.remove_tags(record, ['comments'])

            assert record['comments'] == 'Anything'
