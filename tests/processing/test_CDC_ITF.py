import pandas as pd
from src.processing import CDC_ITF

class Test_add_date_end:

    def test_add_date_end_present(self):

        record = {'measure_stage': 'Lift',
                  'date_start': 'a',
                  'date_end': 'b'}

        record = CDC_ITF.add_date_end(record)

        assert record['date_end'] == 'a'

    def test_add_date_end_absent(self):

        record = {'measure_stage': 'Something Else',
                  'date_start': 'a',
                  'date_end': 'b'}

        record = CDC_ITF.add_date_end(record)

        assert record['date_end'] == 'b'


def test_join_comments():

    record = {'Concise Notes': 'a',
              'Notes': 'b'}

    assert CDC_ITF.join_comments(record) == 'a. b'

class Test_area_covered_national:

    def test_area_covered_national_present(self):

        record = {'area_covered': 'national'}

        res = CDC_ITF.area_covered_national(record)

        assert res['area_covered'] is None

    def test_area_covered_national_absent(self):

        record = {'area_covered': 'something else'}

        res = CDC_ITF.area_covered_national(record)

        assert res['area_covered'] == 'something else'
