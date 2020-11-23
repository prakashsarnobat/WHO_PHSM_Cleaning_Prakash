import re
import pandas as pd


def postprocess(data: pd.DataFrame):
    '''Apply dataset-level transformations to JH_HIT data'''

    data = combine_measures(data, '4.1.2', '_school_closure')
    data = combine_measures(data, '5.7', '_border_air')
    data = combine_measures(data, '5.8', '_border_sea')
    data = combine_measures(data, '5.9', '_border_land')

    return(data)


def combine_measures(data: pd.DataFrame, who_code: str, id_stub: str):
    '''
    Function to combine groups of records with an arbitrary who_code

    Groups are defined by records with identical numeric prop_ids:

    333_school_secondary, 333_school_nursery, 333_school_primary etc.

    or

    234_border_in, 234_border_out

    '''

    # Get records with target who_code
    records = data.copy().loc[data['who_code'] == who_code]

    # Get records without target who_code
    other_data = data.copy().loc[data['who_code'] != who_code, :]

    # Check that no records are being dropped
    assert len(records.index) + len(other_data.index) == len(data.index)

    # Extract numeric values from prop_id_numeric
    records['prop_id_numeric'] = [re.findall(r'\d+', x)[0] for x in records['prop_id']]

    # Split records into groups by numeric id
    records = records.groupby('prop_id_numeric')
    records = [records.get_group(x) for x in records.groups]

    res = []

    for id_group in records:

        group = {}

        for col_name in id_group.columns:

            group[col_name] = list(id_group[col_name].unique())[0]

        group['targeted'] = ', '.join(list(id_group['targeted']))

        group['prop_id'] = group['prop_id_numeric'] + id_stub

        group['dataset'] = 'JH_HIT'

        del group['prop_id_numeric']

        res.append(group)

    res = pd.DataFrame(res)

    data = pd.concat([other_data, res])

    return(data)
