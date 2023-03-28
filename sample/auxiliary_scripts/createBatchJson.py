import json
import glob
import os

dirSongsMscz = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/DickSchmittMscz/"
dirSongsMxl = "/Users/jvo/Downloads/DickSchmittMxl/"

lines = glob.glob(dirSongsMscz + '*' + '.mscz')
# lines = [os.path.basename(line) for line in lines]
lines.sort()

jobs = []

for line in lines:

    line = line.rstrip('\n')

    filename = os.path.basename(line).split("/")[-1]

    outputName = os.path.splitext(filename)[0] + '.musicxml'

    outputPath = dirSongsMxl + outputName

    job = {"in": line,
           "out": outputPath}

    jobs.append(job)

with open("batchJobs.json", "w") as write_file:
    json.dump(jobs, write_file)