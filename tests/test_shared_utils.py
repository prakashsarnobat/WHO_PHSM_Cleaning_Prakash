import os
import shutil
from src import utils
import pytest

class Test_create_dir:

    def test_dir_created(self):
        '''test that a tmp dir is created'''

        utils.create_dir('tmp')

        assert os.path.exists('tmp')

        shutil.rmtree('tmp')

    def test_dir_replaced(self):
        '''test that a tmp dir is replaced if it exists'''

        os.mkdir('tmp')
        os.mkdir('tmp/misc')

        assert os.path.exists('tmp/misc')

        utils.create_dir('tmp')

        assert not os.path.exists('tmp/misc')

        shutil.rmtree('tmp')

@pytest.fixture(scope='session')
def log_line():

    return('TIME - TYPE - KEY=VALUE')


class Test_parse_log:

    def test_parse_log_time(self, log_line):

        parsed = utils.parse_log(log_line)

        assert parsed['timestamp'] == 'TIME'

    def test_parse_log_type(self, log_line):

        parsed = utils.parse_log(log_line)

        assert parsed['type'] == 'TYPE'

    def test_parse_log_message(self, log_line):

        parsed = utils.parse_log(log_line)

        assert parsed['message'] == 'KEY=VALUE'

    def test_parse_log_key(self, log_line):

        parsed = utils.parse_log(log_line)

        assert parsed['key'] == 'KEY'

    def test_parse_log_value(self, log_line):

        parsed = utils.parse_log(log_line)

        assert parsed['value'] == 'VALUE'


    def test_parse_log_errors(self):

        line = 'unformatted'

        with pytest.raises(Exception):
            utils.parse_log(log_line)
