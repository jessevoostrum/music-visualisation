import json
import music21
from matplotlib.transforms import Bbox
from matplotlib.backends.backend_pdf import PdfPages

from Visualiser import Visualiser

dir_notes = '/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/projects/music_software/IFR_animation/notes/'

filename_bass = 'sample_songs_bass.txt'
filename_standards = 'sample_songs.txt'

dir_songs_bass = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/"
dir_songs_standards = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"

f = open('settings.json')
settings = json.load(f)


if False:
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

for line in lines:

    print(line)

    line = line.rstrip('\n')

    streamObj = music21.converter.parse(path_songs + line)

    vis = Visualiser(streamObj, settings)
    vis.generate("output/")
