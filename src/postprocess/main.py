import pandas as pd
from postprocess import CDC_ITF, JH_HIT

def postprocess(data: pd.DataFrame):
    """
    Unify manual changes applied to specific datasets.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataset.

    Returns
    -------
    pd.DataFrame
        Dataset with postprocessing changes applied.

    """

    dataset = list(data['dataset'].unique())[0]

    if dataset == 'CDC_ITF':

        data = CDC_ITF.postprocess(data)

        return(data)

    if dataset == 'JH_HIT':

        data = JH_HIT.postprocess(data)

        return(data)

    else:

        return(data)
