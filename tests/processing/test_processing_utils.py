from src.processing.utils import generate_blank_record


class Test_generate_blank_record:

    def test_is_dict(self):

        assert type(generate_blank_record()) == dict

    def test_dict_key_number(self):

        assert len(generate_blank_record().keys()) == 42
