import pandas as pd
import logging

def postprocess(data: pd.DataFrame):
    '''Apply dataset-level transformations to cdc data'''

    data = remove_id_duplicates(data)

    return(data)


def remove_id_duplicates(data: pd.DataFrame):
    '''Remove duplicate records with identical measure_stage values'''

    n_records = len(data.iloc[:, 1])

    ref_cols = ['country_territory_area',
                'area_covered',
                'prov_subcategory',
                'prov_measure',
                'comments',
                'link',
                'date_start']

    dup_ref = data.groupby(ref_cols).count().reset_index()[ref_cols + ['dataset']]

    dup_ref = dup_ref.loc[dup_ref['dataset'] > 1, :]

    dup_ref.loc[:, 'duplicate'] = True

    dup_ref = dup_ref[ref_cols + ['duplicate']]

    data = pd.merge(data, dup_ref, how='outer', left_on=ref_cols, right_on=ref_cols)

    dups = data.loc[(data['duplicate'] == True) & (data['measure_stage'] == 'Lift'), :].dropna(subset = ['prop_id']).copy()

    dup_ids = dups['prop_id'].unique()

    dups.loc[:, 'who_code'] = 12
    dups.loc[:, 'prov_subcategory'] = 'duplicate'
    dups.loc[:, 'prov_measure'] = 'duplicate'

    data = data.loc[([x not in dup_ids for x in data['prop_id']]), :]

    data = pd.concat([data, dups])

    data = data.drop('duplicate', axis = 1)

    logging.warning('Missing %d CDC Duplicates.' % (n_records - len(data.iloc[:, 1])))

    return(data)
