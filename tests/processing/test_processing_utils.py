import pytest

import pandas as pd
from src.processing.utils import generate_blank_record, key_map, apply_key_map, parse_date, assign_id, assign_who_country_name


class Test_generate_blank_record:

    def test_is_dict(self):

        assert type(generate_blank_record()) == dict

    def test_dict_key_number(self):

        assert len(generate_blank_record().keys()) == 42

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

        a = {'a': None}

        a = assign_id(a)

        assert type(a['who_id']) == str

        assert len(a['who_id']) == 36

class Test_assign_who_country_name:

    def test_assign_who_country_name(self):

        a = {'iso': 'AFG'}
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

        a = {'iso': 'AFG'}

        country_ref = pd.DataFrame({'iso': ['USA']})

        with pytest.raises(KeyError):
            assign_who_country_name(a, country_ref)
