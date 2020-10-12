import pandas as pd
from src.preprocess import column_map


def test_column_map():

    df = pd.DataFrame({'a': [1, 2, 3, 4]})

    res = column_map.column_map(df, 'a', 'b')

    assert res.columns == ['b']
