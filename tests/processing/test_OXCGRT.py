import pytest
from src.processing import OXCGRT

class Test_label_update_phrase:

    def test_label_update_phrase_is_phrase(self):
        '''
        Test that the corret values are inserted when the
        comments include a no update phrase
        '''

        record = {'comments': 'No changes',
                  'who_code': None,
                  'who_category': None,
                  'who_subcategory': None,
                  'who_measure': None}

        res = OXCGRT.label_update_phrase(record, ['No changes'])

        assert res['who_code'] == '10'
        assert res['who_category'] == 'Not of interest'
        assert res['who_subcategory'] == 'Not of interest'
        assert res['who_measure'] == 'Not of interest'

    def test_label_update_phrase_is_phrase(self):
        '''
        Test that the corret values are inserted when the
        comments include a no update phrase
        '''

        record = {'comments': 'This is legit',
                  'who_code': None,
                  'who_category': None,
                  'who_subcategory': None,
                  'who_measure': None}

        res = OXCGRT.label_update_phrase(record, ['No changes'])

        assert res['who_code'] is None
        assert res['who_category'] is None
        assert res['who_subcategory'] is None
        assert res['who_measure'] is None

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


class Test_get_comment_links:
    '''Test that comments are correctly extracted from links'''

    def test_get_comment_links_single_link(self):

        link = 'https://github.com/lshtm-gis/WHO_PHSM_Cleaning'

        comments = 'This is a comment with a link here: ' + link

        res = OXCGRT.get_comment_links(comments)

        assert len(res) == 1
        assert res[0] == link

    def test_get_comment_links_multiple_links(self):

        link = 'https://github.com/lshtm-gis/WHO_PHSM_Cleaning'

        comments = 'This is a comment with a link here: ' + link + ' And also this one! ' + link

        res = OXCGRT.get_comment_links(comments)

        assert len(res) == 2
        assert res[0] == link
        assert res[1] == link

    def test_get_comment_links_complicated(self):

        link = 'https://www.google.com/search?q=non+pharmaceutical+interventions&oq=non+pharma&aqs=chrome.1.0i457j0j69i57j0l5.4434j0j7&sourceid=chrome&ie=UTF-8'

        comments = 'This says somethign else ' + link

        res = OXCGRT.get_comment_links(comments)

        assert len(res) == 1
        assert res[0] == link

class Test_assign_comment_links:

    def test_assign_comment_links_single(self):

        link = 'https://github.com/lshtm-gis/WHO_PHSM_Cleaning'

        record = {'comments': 'This is a comment with a link here: ' + link,
                  'link': None,
                  'alt_link': None}

        res = OXCGRT.assign_comment_links(record)

        assert res['link'] == link
        assert res['alt_link'] is None

    def test_assign_comment_links_multiple(self):

        link1 = 'https://github.com/lshtm-gis/WHO_PHSM_Cleaning'
        link2 = 'https://github.com/lshtm-gis/WHO_PHSM_Cleaning/OTHER_THING'

        record = {'comments': 'This is a comment with a link here: ' + link1 + ' And here ' + link2,
                  'link': None,
                  'alt_link': None}

        res = OXCGRT.assign_comment_links(record)

        assert res['link'] == link1
        assert res['alt_link'] == link2
