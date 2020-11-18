import pytest
from src.processing import OXCGRT

class Test_is_update_phrase:
    '''Test that is_no_update_phrase correctly identifies no update records'''

    def test_is_update_phrase_is_update(self):

        comment = 'This is actually an update'

        res = OXCGRT.is_update_phrase(comment, ['^No changes'])

        assert res == False

    def test_is_update_phrase_is_not_update(self):

        comment = 'No changes'

        res = OXCGRT.is_update_phrase(comment, ['^No changes'])

        assert res == True

    def test_is_update_phrase_is_not_update_long(self):

        comment = 'No changes. And this is other text that we do not care about.'

        res = OXCGRT.is_update_phrase(comment, ['^No changes'])

        assert res == True

    def test_is_update_phrase_none(self):

        comment = None

        res = OXCGRT.is_update_phrase(comment, ['^No changes'])

        assert res == False
