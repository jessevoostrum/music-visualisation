import json
import music21

from Visualiser import Visualiser


dir_songs_standards = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"

dir_notes = '/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/projects/music_software/IFR_animation/notes/'
filename_standards = 'sample_songs.txt'

path_note = dir_notes + filename_standards
path_songs = dir_songs_standards

d = open('modeSongs.json')
modeSongs = json.load(d)

with open(path_note) as f:
    lines = f.readlines()

for line in lines:

    print(line)

    line = line.rstrip('\n')

    streamObj = music21.converter.parse(path_songs + line)

    try:
        songTitle = streamObj.metadata.title
    except:
        print('no title')
        next()

    if songTitle in modeSongs:
        if not modeSongs[songTitle] == '':
            mode = modeSongs[songTitle]
            keySingature = streamObj[music21.key.KeySignature].first()
            firstMeasure = streamObj[music21.stream.Measure].first()
            firstMeasure.keySignature = keySingature.asKey(mode)
            streamObj.write("musicxml", "sheetMusic/" + line)

    else:
        keySingature = streamObj[music21.key.KeySignature].first()
        if type(keySingature) == music21.key.Key:
            modeSongs[songTitle] = keySingature.mode
        else:
            modeSongs[songTitle] = ""

e = open('modeSongs.json', 'w')
json.dump(modeSongs, e, indent=4)

