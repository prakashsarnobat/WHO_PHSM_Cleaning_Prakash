import os
import shutil
from src import utils

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
