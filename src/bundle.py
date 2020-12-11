"""
bundle.py

Script to bundle output datasets from the tmp directory
into the data directory.

"""

import os
import shutil
from datetime import datetime

print('Creating output bundle...')

# Define output directory
out_dir = 'data/output'

# Try to remove output directory if it exists
try:

    shutil.rmtree(out_dir)

except Exception:

    pass

# Create a new empty output directory
os.mkdir(out_dir)

# Define date string of today's date
date_string = datetime.today().strftime('%Y_%m_%d')

# Locate datasets to be moved to output directory
master = 'tmp/master/master.csv'
id_ref = 'tmp/master/id_ref.csv'
release = 'tmp/master/release.csv'

# Locate reports to be moved to output directory
technical_report = 'reporting/technical_report.html'
summary_report = 'reporting/summary_report.html'

# Define name of files to be added to output directory
output_master = out_dir + '/master_' + date_string + '.csv'
output_id_ref = out_dir + '/id_ref_' + date_string + '.csv'
output_release = out_dir + '/release_' + date_string + '.csv'

# Define name of reports to be added to output directory
output_technical_report = out_dir + '/technical_report.html'
output_summary_report = out_dir + '/summary_report.html'

# Define name of files to be added to not_cleansed directory
not_cleansed_master = 'data/not_cleansed/master_latest.csv'
not_cleansed_master_latest = 'data/not_cleansed/master_' + date_string + '.csv'

# Define name of zip archive
zip_archive = 'data/output_' + date_string

# Move files to defined locations in the output folder
shutil.copy(master, output_master)
shutil.copy(release, output_release)
shutil.copy(id_ref, output_id_ref)

# Move files to defined locations in the not_cleansed directory
shutil.copy(master, not_cleansed_master)
shutil.copy(master, not_cleansed_master_latest)

# Move reports to defined locations in the output folder
shutil.copy(technical_report, output_technical_report)
shutil.copy(summary_report, output_summary_report)

# Make a zip file of the output directory
shutil.make_archive(zip_archive, 'zip', out_dir)

print('Success.')
