import pandas as pd
from CDC_ITF

def postprocess(data: pd.DataFrame):
    '''Function to apply manual changes to individual records'''

    dataset = list(data['dataset'].unique())[0]

    if dataset == 'CDC_ITF':

        data = CDC_ITF.postprocess(data)
        print(data)

    else:

        return(data)
