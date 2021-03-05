import pandas as pd


def postprocess(data: pd.DataFrame):
    """
    Apply dataset-level transformations to EURO data.

    Parameters
    ----------
    data : pd.DataFrame
        Input who_code code.

    Returns
    -------
    pd.DataFrame
        Euro data with only the specified who_code.

    """
    # Read the who_code to be postprocess for the week
    euro_weekly_upload = pd.read_csv('config/euro_weekly_upload/EURO.csv', dtype={'who_code':str})
    
    data = weekly_import(data, euro_weekly_upload)

    return(data)

    
def weekly_import(data: pd.DataFrame, who_code:pd.DataFrame):
    """
    EURO data are imported progressively
    
    Retrieve only `who_code` provided in `config/euro_weekly_upload` for postprocessing.

    Parameters
    ----------
    data : pd.DataFrame
        Input data.
    
    who_code : pd.DataFrame
        `who_code` to postprocess.

    Returns
    -------
    pd.DataFrame
        Euro data with only the specified who_code..

    """

    # Return only data that contain the who_code for the week
    data = data.loc[data['who_code'].isin(who_code['who_code'])].copy()
    
    return(data)
