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
    # Get records with target who_code
    euro_weekly_upload = pd.read_csv('config/euro_weekly_upload/EURO.csv', dtype={'who_code':str})
    

    # Get records without target who_code
    data = data.loc[data['who_code'].isin(euro_weekly_upload['who_code'])].copy()
    
    return(data)
