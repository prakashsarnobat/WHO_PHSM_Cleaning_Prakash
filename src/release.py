"""
release.py

Script to move latest data to release repository
"""
import os
import sys
from datetime import datetime
from shutil import copyfile

release_repo = '../WHO-PHSM'

try:

    assert os.path.exists(release_repo)

except Exception:

    raise FileNotFoundError('Unable to locate release repository.')

print()
response_check = input('Are you sure you want to create a new release? (y/n)')

if response_check != 'y':

    raise SystemError('Cancelled.')

date_now = datetime.now().strftime('%Y_%m_%d')

release_latest = 'data/output/release_{}.csv'.format(date_now)

repo_release_log = release_repo + '/data/release_{}.csv'.format(date_now)

repo_release_latest = release_repo + '/data/release_latest.csv'

copyfile(release_latest, repo_release_log)
copyfile(release_latest, repo_release_latest)
print('Success.')
