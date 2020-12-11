import pandas as pd
import logging
from datetime import datetime


def check_input(records: pd.DataFrame, column_config: pd.DataFrame, date_config: pd.DataFrame, dataset: str):
    """
    Function to unify all input checks.

    Parameters
    ----------
    records : pd.DataFrame
        Dataframe of provider data.
    column_config : pd.DataFrame
        Reference for accepted column names.
    date_config : pd.DataFrame
        Reference for accepted date formats.
    dataset : str
        Name of provider dataset.

    Returns
    -------
    type
        Description of returned object.

    """

    check_column_names(records, column_config)

    check_date_format(records, date_config, dataset)


def check_column_names(records: pd.DataFrame, config: pd.DataFrame, log: bool = True):
    """
    Function to check that column names agree with config or raise exception.

    Parameters
    ----------
    records : pd.DataFrame
        Dataframe of provider data.
    config : pd.DataFrame
        Reference for accepted column names.
    log : bool
        Whether or not to log results of checks.

    Returns
    -------
    None

    """

    dataset = list(config['dataset'].unique())[0]

    try:

        assert set(records.columns) == set(config['column'])

        if log:

            logging.info('INPUT_CHECK_SUCCESS=%s input columns OK.' % dataset)

    except Exception as e:

        present_in_input = set(records.columns).difference(set(config['column']))
        present_in_config = set(config['column']).difference(set(records.columns))

        message = 'INPUT_CHECK_FAILURE=Unexpected %s columns. Present in input: %s, present in config: %s' % (dataset, present_in_input, present_in_config)

        if log:

            logging.info(message)

        #raise e


def check_date_format(data: pd.DataFrame,
                      config: pd.DataFrame,
                      dataset: str,
                      log: bool = True):
    """
    Check that an input date is in the expected format.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe of provider data..
    config : pd.DataFrame
        Reference for accepted date formats.
    dataset : str
        Name of provider dataset.
    log : bool
        Whether or not to log results of checks.

    Returns
    -------
    None

    """

    format = config.loc[config['dataset'] == dataset, 'format'].item()
    date_column = config.loc[config['dataset'] == dataset, 'date_column'].item()

    res = [validate_date_format(x, format) for x in data[date_column] if x is None]

    try:

        assert len(res) == 0

        if log:

            logging.info('INPUT_CHECK_SUCCESS=%s %s date format is %s.' % (dataset, date_column, format))

    except Exception:

        if log:

            logging.info('INPUT_CHECK_FAILURE=%s %s %d dates not in the format %s.' % (dataset, date_column, len(res), format))


def validate_date_format(date, format):
    """
    Return None if a date format does not parse.

    Parameters
    ----------
    date : type
        Input date string.
    format : type
        Input accpeted format to try.

    Returns
    -------
    type
        Returns date on successful parse or None on parsing failure.

    """

    try:

        return(datetime.strptime(date, format))

    except Exception:

        return(None)
