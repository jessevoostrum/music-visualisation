import json
import music21
import glob
import os


dir_songs_standards = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"
dir_songs_bass = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/"


d = open('integerbook/auxiliary_scripts/modeSongs.json')
modeSongs = json.load(d)

# dir_notes = '/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/projects/music_software/IFR_animation/notes/'
# filename_standards = 'sample_songs.txt'
#
# path_note = dir_notes + filename_standards
# path_songs = dir_songs_standards
#

#
# with open(path_note) as f:
#     lines = f.readlines()


dirSongs = dir_songs_bass


lines = glob.glob(dirSongs + '*' + '.mxl')
lines = [os.path.basename(line) for line in lines]
lines.sort()


for line in lines:

    print(line)

    line = line.rstrip('\n')

    streamObj = music21.converter.parse(dirSongs + line)

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
        keySignature = streamObj[music21.key.KeySignature].first()
        # check if the key contains info about the mode.
        # this is only the case when it is a key.Key instead of a ? key symbol / signature
        if type(keySignature) == music21.key.Key:
            modeSongs[songTitle] = keySignature.mode
        else:
            modeSongs[songTitle] = ""

e = open('modeSongs.json', 'w')
json.dump(modeSongs, e, indent=4)

