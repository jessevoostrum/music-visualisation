import glob
import os
import shutil
import music21

dirSongsOriginal = "/Users/jvo/Downloads/DickSchmittMxl/"
dirSongs = "/Users/jvo/Documents/hello-app/sheets/"


lines = glob.glob(dirSongsOriginal + '*' + '.musicxml')
lines = [os.path.basename(line) for line in lines]
lines.sort()


for line in lines:

    print(line)

    try:
        pathSong = dirSongsOriginal + line

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