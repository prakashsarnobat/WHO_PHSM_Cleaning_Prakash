import pandas as pd
from src.processing import ACAPS

class Test_replace_country:

    def test_replace_country_present(self):

        country_name = 'Denmark'
        area_name = 'Greenland'

        record = {'country_territory_area':country_name,
                  'area_covered':area_name}

        res = ACAPS.replace_country(record, country_name, area_name)

        assert res['country_territory_area'] == area_name

        assert res['area_covered'] is None

    def test_replace_country_absent(self):

        country_name = 'Denmark'
        area_name = 'Greenland'

        record = {'country_territory_area':country_name,
                  'area_covered':area_name}

        res = ACAPS.replace_country(record, country_name, 'Something else')

        assert res['country_territory_area'] == country_name

        assert res['area_covered'] == area_name
