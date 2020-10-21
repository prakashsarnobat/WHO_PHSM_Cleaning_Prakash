import pickle
from utils import parse_log

#parse logs here
preprocess_path = 'tmp/preprocess/preprocess.log'
process_logs = 'tmp/process/process.log'
postprocess_logs = 'tmp/postprocess/postprocess.log'

preprocess = open(preprocess_path, 'r').readlines()
process = open(process_logs, 'r').readlines()
postprocess = open(postprocess_logs, 'r').readlines()

logs = {'preprocess': [],
        'process': [],
        'postprocess': []}

# parse preprocessing logs
for line in preprocess:

    logs['preprocess'].append(parse_log(line))

#parse processing logs
for line in process:

    logs['process'].append(parse_log(line))

# parse postprocessing logs
for line in postprocess:

    logs['postprocess'].append(parse_log(line))

print(logs)



#output log data in easy format

#make report with make
