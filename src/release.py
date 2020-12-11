"""
release.py

Script to move latest data to release repository
"""
import os
from datetime import datetime
from shutil import copyfile

# Define repository where data is released
release_repo = '../WHO-PHSM'

# Throw error if release repo is not found
try:

    assert os.path.exists(release_repo)

except Exception:

    raise FileNotFoundError('Unable to locate release repository.')


# Prompt to check that data should be released
response_check = input('Are you sure you want to create a new release? (y/n)')

# Abort if input is not 'y'
if response_check != 'y':

    raise SystemError('Cancelled.')

# Format date string for current date
date_now = datetime.now().strftime('%Y_%m_%d')

# Define file name release in output directory
release_latest = 'data/output/release_{}.csv'.format(date_now)

# Define file name of release for log
repo_release_log = release_repo + '/data/release_{}.csv'.format(date_now)

# Define file name of latest release
repo_release_latest = release_repo + '/data/release_latest.csv'

# Move release files to release repository
copyfile(release_latest, repo_release_log)
copyfile(release_latest, repo_release_latest)

print('Success.')
