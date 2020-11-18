'''

Script to add uuid to existing records

Also shifts who_code values to original_who_code

'''
import uuid
import pandas as pd

manually_cleaned = pd.read_csv('data/cleansed/mistress_latest_old.csv', low_memory=False)

manually_cleaned['uuid'] = [str(uuid.uuid4()) for x in manually_cleaned.iloc[:, 1]]

manually_cleaned['original_who_code'] = manually_cleaned['who_code']

manually_cleaned.to_csv('data/cleansed/mistress_latest.csv', index = False)
