import pytest

from src.processing.utils import generate_blank_record, key_map, apply_key_map


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
