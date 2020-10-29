import pytest
import pandas as pd
from src.manually_cleaned import main

class Test_update_following_measures():

    def test_update_following_measures(self):

        data = pd.DataFrame({
            'who_id': ['1', '2'],
            'date_start': ['1', 'NEW_DATE_END'],
            'date_end': [None, None],
            'reason_ended': [None, None],
            'measure_stage': [None, 'NEW_REASON_ENDED'],
            'following_measure_number': ['2', None]
        })

        res = main.update_following_measures(data)

        assert list(res.loc[0, 'date_end'])[0] == 'NEW_DATE_END'
        assert list(res.loc[0, 'reason_ended'])[0] == 'NEW_REASON_ENDED'

    def test_update_following_measures_missing(self):

        data = pd.DataFrame({
            'who_id': ['1', '3'],
            'date_start': ['1', 'NEW_DATE_END'],
            'date_end': ['PREV_DATE_END', None],
            'reason_ended': ['PREV_REASON_ENDED', None],
            'measure_stage': [None, 'NEW_REASON_ENDED'],
            'following_measure_number': ['2', None]
        })

        res = main.update_following_measures(data)

        assert res.loc[0, 'date_end'] == 'PREV_DATE_END'
        assert res.loc[0, 'reason_ended'] == 'PREV_REASON_ENDED'


class Test_update_measure_stage_date():

    def test_update_measure_stage_date(self):

        data = pd.DataFrame({
            'measure_stage': ['finish'],
            'date_start': ['1'],
            'date_end': [None],
            'reason_ended': [None]
        })

        res = main.update_measure_stage_date(data)

        assert res.loc[0, 'date_end'] == '1'
        assert res.loc[0, 'reason_ended'] == 'finish'

    def test_update_measure_stage_date_passes(self):

        data = pd.DataFrame({
            'measure_stage': ['anything'],
            'date_start': ['1'],
            'date_end': [None],
            'reason_ended': [None]
        })

        res = main.update_measure_stage_date(data)

        assert res.loc[0, 'date_end'] == None
        assert res.loc[0, 'reason_ended'] == None
