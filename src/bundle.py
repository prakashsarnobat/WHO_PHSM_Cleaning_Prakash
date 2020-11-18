"""
bundle.py

Script to bundle output datasets from the tmp directory
into the data directory.

"""

from datetime import datetime
import shutil

date_string = datetime.today().strftime('%Y_%m_%d')

master = 'tmp/master/master.csv'
id_ref = 'tmp/master/id_ref.csv'

technical_report = 'reporting/technical_report.html'
summary_report = 'reporting/summary_report.html'

zip_dir = 'data/output'

output_master = 'data/output/master_' + date_string + '.csv'
output_id_ref = 'data/output/id_ref_' + date_string + '.csv'

output_technical_report = 'data/output/technical_report.html'
output_summary_report = 'data/output/summary_report.html'

not_cleansed_master = 'data/not_cleansed/master_latest.csv'
not_cleansed_master_latest = 'data/not_cleansed/master_' + date_string + '.csv'

zip_archive = 'data/output_' + date_string

# Move master to locations in the output folder
shutil.copy(master, output_master)
shutil.copy(master, not_cleansed_master)
shutil.copy(master, not_cleansed_master_latest)

# Move id ref to output folder
shutil.copy(id_ref, output_id_ref)

# Move technical report to output folder
shutil.copy(technical_report, output_technical_report)

# Move summary report to output folder
shutil.copy(summary_report, output_summary_report)

# Make a zip file of the output
shutil.make_archive(zip_archive, 'zip', zip_dir)
