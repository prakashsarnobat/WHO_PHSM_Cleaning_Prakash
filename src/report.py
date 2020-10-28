import pickle
from utils import parse_log

print('Parsing logs...')

preprocess_path = 'tmp/preprocess/preprocess.log'
process_logs = 'tmp/process/process.log'
postprocess_logs = 'tmp/postprocess/postprocess.log'
combine_logs = 'tmp/combine/combine.log'

preprocess = open(preprocess_path, 'r').readlines()
process = open(process_logs, 'r').readlines()
postprocess = open(postprocess_logs, 'r').readlines()
combine = open(combine_logs, 'r').readlines()

logs = {'preprocess': [],
        'process': [],
        'postprocess': [],
        'combine': []}

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
for line in combine:

    logs['combine'].append(parse_log(line))

print('Writing report.pickle...')

pickle.dump(logs, open("tmp/report.pickle", "wb"))

print('Success.')
