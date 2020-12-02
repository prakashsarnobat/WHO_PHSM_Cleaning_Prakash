import logging
import pandas as pd
import numpy as np

try:

    from src.processing.utils import generate_blank_record

except:

    from processing.utils import generate_blank_record


def check_output(data: pd.DataFrame):
    '''Function to check output from master, mistress, and output'''

    # check columns are correct
    check_column_names(data)

    # check duplicate who_id
    check_duplicate_id(data, 'uuid')
    check_duplicate_id(data, 'who_id')

    # check for coded values from config
    coded_config = pd.read_csv('config/output_check/coded_values.csv')
    check_coded_values(data, coded_config)

    # check for one to one relationships between two columns
    check_columns_one_to_one(data, 'iso', 'country_territory_area')
    check_columns_one_to_one(data, 'iso', 'who_region')
    check_columns_one_to_one(data, 'iso', 'iso_3166_1_numeric')

    # check for unknown who_codes and iso_codes
    check_unknown_values(data, 'iso_3166_1_numeric')
    check_unknown_values(data, 'who_region')
    check_unknown_values(data, 'country_territory_area')
    check_unknown_values(data, 'who_code')
    check_unknown_values(data, 'who_measure')
    check_unknown_values(data, 'who_subcategory')
    check_unknown_values(data, 'who_category')

    check_values_present(data, 'duplicate_record_id', 'who_id')
    check_values_present(data, 'prev_measure_number', 'who_id')
    check_values_present(data, 'following_measure_number', 'who_id')

    return(data)


def check_duplicate_id(data: pd.DataFrame, key: str, log: bool = True):

    res = len(data[key]) == len(data[key].unique())

    try:

        assert res

        if log:

            logging.info('OUTPUT_CHECK_SUCCESS=No Duplicate %s.' % key)

    except Exception as e:

        if log:

            logging.error('OUTPUT_CHECK_FAILURE=Duplicate %s detected.' % key)

        pass

    return(res)


def check_column_names(data: pd.DataFrame, log: bool = True):
    '''Function to check that column names are expected'''
    expected = generate_blank_record().keys()

    try:

        assert set(data.columns) == set(expected)

        if log:

            logging.info('OUTPUT_CHECK_SUCCESS=Data has expected column names.')

    except Exception as e:

        exp_diff = set(expected).difference(set(data.columns))
        new_diff = set(data.columns).difference(set(expected))

        if log:

            if len(exp_diff) > 0:

                logging.error('OUTPUT_CHECK_FAILURE=Column names do not agree. Present in expected: %s' % ', '.join(list(exp_diff)))

            if len(new_diff) > 0:

                logging.error('OUTPUT_CHECK_FAILURE=Column names do not agree. Present in input: %s' % ', '.join(list(new_diff)))

        pass


def check_unknown_values(data: pd.DataFrame, key: str, log: bool = True):
    '''Function to check for unknown values'''

    unknown_vals = data.loc[data[key] == 'unknown']

    datasets = list(unknown_vals['dataset'].unique())
    datasets = ', '.join(datasets)

    n_unknown = len(unknown_vals.iloc[:, 1])

    try:

        assert n_unknown == 0

        if log:

            logging.info('OUTPUT_CHECK_SUCCESS=No unknown values in %s.' % key)

    except Exception as e:

        if log:

            logging.error('OUTPUT_CHECK_FAILURE=%d unknown values in %s.' % (n_unknown, key))

            country_keys = ['iso', 'iso_3166_1_numeric', 'who_region', 'country_territory_area']
            coding_keys = ['who_code', 'who_measure', 'who_subcategory', 'who_category', 'prov_category', 'prov_subcategory', 'prov_measure']

            if key in country_keys:

                unknown_vals = unknown_vals[country_keys].drop_duplicates()

                for k, row in unknown_vals.iterrows():

                    logging.error('OUTPUT_CHECK_FAILURE=Unknown country in dataset: %s; %s.' % (datasets, ' '.join(['%s=%s' % (key, value) for (key, value) in row.items()])))

            elif key in coding_keys:

                unknown_vals = unknown_vals[coding_keys].drop_duplicates()

                for k, row in unknown_vals.iterrows():

                    logging.error('OUTPUT_CHECK_FAILURE=Unknown coding in dataset: %s; %s.' % (datasets, ' '.join(['%s: %s' % (key, value) for (key, value) in row.items()])))

        pass


def check_values_present(data: pd.DataFrame, focus_col: str, ref_col: str, log: bool = True):
    '''Function to check if values present in one column can also be found in another column'''

    diff = list(set(data[focus_col].dropna()).difference(set(data[ref_col].dropna())))

    res = len(diff) == 0

    try:

        assert res

        if log:

            logging.info('OUTPUT_CHECK_SUCCESS=All values in %s are present in %s.' % (focus_col, ref_col))

    except:

        if log:

            logging.info('OUTPUT_CHECK_FAILURE=%d values in %s are missing from %s.' % (len(diff), focus_col, ref_col))

        pass

    return(res)


def check_coded_values(data: pd.DataFrame, config: pd.DataFrame, log: bool = True):
    '''Function to check for any values not accepted as coded values'''

    config = config.groupby('column')
    config = [config.get_group(x) for x in config.groups]

    for column in config:

        column_name = list(column['column'].unique())[0]

        expected = list(column['value']) + [None]

        obs = list(data[column_name].unique())

        # Does not detect nan values
        obs = [x for x in obs if str(x) != 'nan']

        difference = set(obs).difference(set(expected))

        try:

            assert len(difference) == 0

            if log:

                logging.info('OUTPUT_CHECK_SUCCESS=No unexpected values in %s.' % column_name)

        except Exception as e:

            if log:

                logging.error('OUTPUT_CHECK_FAILURE=Unexpected values in %s: %s.' % (column_name, ', '.join([str(x) for x in difference])))

            pass


def check_columns_one_to_one(data: pd.DataFrame, ref_col: str, target_col: str, log: bool = True):
    '''
    Function to detect violations of one-to-one relationships in a pair of columns.
    '''

    data = data.copy()

    data = data[[ref_col, target_col]].drop_duplicates()

    res = data.groupby([ref_col]).count()

    res = list(res[target_col].unique())

    try:

        assert res == [1]

        if log:

            logging.info('OUTPUT_CHECK_SUCCESS=No one-to-one violations found between %s and %s.' % (ref_col, target_col))

    except Exception as e:

        if log:

            logging.error('OUTPUT_CHECK_FAILURE=Violation of one-to-one relationship between %s and %s.' % (ref_col, target_col))

        pass

    return(res)
