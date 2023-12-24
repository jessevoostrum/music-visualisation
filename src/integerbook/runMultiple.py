import json
import glob
import os

from integerbook.main import Visualiser

dirSongs = "/Users/jvo/Documents/programming/sheet-music/sheets/christmas-selection"
outputDir = "/Users/jvo/Downloads/output-christmas-selection"


f = open('settings.json')
settings = json.load(f)

settings["measuresPerLine"] = 4
settings["subdivision"] = 0
settings['thickBarlines'] = True

settings["setInMajorKey"] = True

settings["lyrics"] = True

settings['coloursVoices'] = True

# settings['fontDirectory'] = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/fonts/Vulf Mono/Vulf Mono/Desktop/"
# settings['font'] = 'Vulf Mono'
# settings['fontStyle'] = 'italic'
# settings['fontWeight'] = 'light'
settings['printArranger'] = False
settings["chordVerbosity"] = 1
settings["romanNumerals"] = True

lines = glob.glob(dirSongs + '/' + '*' + '.musicxml')
lines = [os.path.basename(line) for line in lines]
lines.sort()


for line in lines:

    print(line)

    try:
        pathSong = dirSongs + '/' + line

        vis = Visualiser(pathSong, settings)

        vis.saveFig(dirName=outputDir)

    except Exception as e:
        print("ERROR", "\n")
        print(repr(e))

