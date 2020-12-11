import pickle
from utils import parse_log

print('Parsing logs...')

# Define paths to log files
preprocess_path = 'tmp/preprocess/preprocess.log'
process_logs = 'tmp/process/process.log'
postprocess_logs = 'tmp/postprocess/postprocess.log'
manually_cleaned_logs = 'tmp/manually_cleaned/manually_cleaned.log'
master_logs = 'tmp/master/master.log'

# Open each log file
preprocess = open(preprocess_path, 'r').readlines()
process = open(process_logs, 'r').readlines()
postprocess = open(postprocess_logs, 'r').readlines()
manually_cleaned = open(manually_cleaned_logs, 'r').readlines()
master = open(master_logs, 'r').readlines()

# Define dict to store log contents
logs = {'preprocess': [],
        'process': [],
        'postprocess': [],
        'manually_cleaned': [],
        'master': []}

# parse preprocessing logs
for line in preprocess:

    logs['preprocess'].append(parse_log(line))

# parse processing logs
for line in process:

    logs['process'].append(parse_log(line))

# parse postprocessing logs
for line in postprocess:

    logs['postprocess'].append(parse_log(line))

# parse combine logs
for line in manually_cleaned:

    logs['manually_cleaned'].append(parse_log(line))

for line in master:

    logs['master'].append(parse_log(line))

print('Writing report.pickle...')

# Write report content as pickle object
pickle.dump(logs, open("tmp/report.pickle", "wb"))

print('Success.')
