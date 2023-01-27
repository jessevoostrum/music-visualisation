import json
import glob
import os

dirSongs = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/DickSchmitt/"

lines = glob.glob(dirSongs + '*' + '.mscz')
# lines = [os.path.basename(line) for line in lines]
lines.sort()

jobs = []

for line in lines:

    line = line.rstrip('\n')

    outputName = os.path.splitext(line)[0] + '.musicxml'

    job = {"in": line,
           "out": outputName}

    jobs.append(job)

with open("batchJobs.json", "w") as write_file:
    json.dump(jobs, write_file)