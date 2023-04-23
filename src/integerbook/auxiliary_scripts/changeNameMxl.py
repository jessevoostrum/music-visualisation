import glob
import os
import shutil
import music21

dirSongs2 = "/Users/jvo/Documents/hello-app/sheets(2)/"
dirSongs = "/Users/jvo/Documents/hello-app/sheets/"


lines = glob.glob(dirSongs2 + '*' + '.musicxml')
lines = [os.path.basename(line) for line in lines]
lines.sort()


for line in lines:

    print(line)

    try:
        pathSong = dirSongs2 + line

        s = music21.converter.parse(pathSong)

        try:
            songTitle = s.metadata.bestTitle
        except:
            songTitle = "no title"
            print("!!!no title", pathSong)

        newPathSong = dirSongs + songTitle + ".musicxml"

        shutil.copy(pathSong, newPathSong)

    except Exception as e:
        print("ERROR", "\n")
        print(repr(e))