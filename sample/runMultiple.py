import json
import music21
import glob
import os

from sample.main import Visualiser

# dir_notes = '/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/projects/music_software/IFR_animation/notes/'
dir_notes = '../notes/'

filename_bass = 'sample_songs_bass.txt'
# filename_standards = 'sample_songs.txt'
filename_standards = 'standards.txt'


dir_songs_bass = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/"
dir_songs_standards = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"

f = open('settings.json')
settings = json.load(f)


if True:
    path_note = dir_notes + filename_standards
    path_songs = dir_songs_standards

else:
    path_note = dir_notes + filename_bass
    path_songs = dir_songs_bass
    settings["offsetLineMax"] = 8
    settings["subdivision"] = 2
    # settings["setInMajorKey"]=False

with open(path_note) as f:
    lines = f.readlines()


dirStandards = dir_songs_standards

lines = glob.glob(dirStandards + '*' + '.mxl')
lines = [os.path.basename(line) for line in lines]
lines.sort()

for line in lines:

    print(line)

    line = line.rstrip('\n')

    try:
        streamObj = music21.converter.parse(path_songs + line)

        vis = Visualiser(streamObj, settings)

        vis.generate("output-standards/")
    except:
        pass
