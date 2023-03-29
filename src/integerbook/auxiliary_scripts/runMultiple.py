import json
import glob
import os

from integerbook.main import Visualiser


dir_songs_bass = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/"
dir_songs_standards = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"
dir_songs_testsuite = "/Users/jvo/Documents/music-visualisation/testsuite/"
dir_songs_DS = "/Users/jvo/Downloads/DickSchmittMxl/"

dirSongs = dir_songs_DS


f = open('../settings.json')
settings = json.load(f)

settings["measuresPerLine"] = 4
settings["subdivision"] = 0
settings["setInMajorKey"] = True
settings["lyrics"] = False
settings['coloursVoices'] = False
settings['coloursCircleOfFifths'] = False
settings['thickBarlines'] = True

settings['fontDirectory'] = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/fonts/Vulf Mono/Vulf Mono/Desktop/"
settings['font'] = 'Vulf Mono'
settings['fontStyle'] = 'italic'
settings['fontWeight'] = 'light'
settings['printArranger'] = False


lines1 = glob.glob(dirSongs + '*' + '.mxl')
lines2 = glob.glob(dirSongs + '*' + '.musicxml')
lines = lines1 + lines2
lines = [os.path.basename(line) for line in lines]
lines.sort()


for line in lines:

    print(line)

    line = line.rstrip('\n')

    try:
        pathSong = dirSongs + line

        vis = Visualiser(pathSong, settings)
        vis.generate("../../output/outputDickSchmitt/")

    except Exception as e:
        print("ERROR", "\n")
        print(repr(e))

