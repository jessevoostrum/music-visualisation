import glob
import os

import music21


def separateBookIntoSongs(book):
    s = book

    # renumber measure
    for i, measure in enumerate(s[music21.stream.Measure]):

        measure.number = i + 1
        measure.informSites()

    offsetsStartPage = [0] + [el.getOffsetInHierarchy(s) for el in s[music21.layout.PageLayout]]

    metadataPerPage = [[page, None, None] for page in range(1, len(offsetsStartPage) + 1)]

    for tb in s[music21.text.TextBox]:
        if tb.page > len(offsetsStartPage):
            continue

        if tb.style.justify == 'right':
            metadataPerPage[tb.page - 1][2] = tb.content

        if tb.style.justify == 'center' and not metadataPerPage[tb.page - 1][1]:
            metadataPerPage[tb.page - 1][1] = tb.content

    noStartIdx = []

    for i, datum in enumerate(metadataPerPage):
        if not datum[2]:
            noStartIdx.append(i)

    offsetsStartSong = [offset for i, offset in enumerate(offsetsStartPage) if i not in noStartIdx]
    metadataSongs = [datum for i, datum in enumerate(metadataPerPage) if i not in noStartIdx]

    measureNumbersStartSong = []
    measures = s[music21.stream.Measure]
    j = 1
    for i in range(len(measures)):
        if measures[i].offset in offsetsStartSong:
            measureNumbersStartSong.append(measures[i].number)

    measureNumbersStartEndSong = []

    for measureNumberStart, measureNumberStartNext in zip(measureNumbersStartSong, measureNumbersStartSong[1:]):
        measureNumbersStartEndSong.append((measureNumberStart, measureNumberStartNext - 1))

    lastMeasureNumber = s[music21.stream.Measure][-1].number
    measureNumbersStartEndSong.append((measureNumbersStartSong[-1], lastMeasureNumber))

    songs = []

    for measureNumberStart, measureNumberEnd in measureNumbersStartEndSong:
        songs.append(s.measures(measureNumberStart, measureNumberEnd))

    for i, song in enumerate(songs):
        song.insert(0, music21.metadata.Metadata())
        song.metadata.title = metadataSongs[i][1]
        song.metadata.composer = metadataSongs[i][2]

    return songs

def cleanSong(song):
    s = song

    # remove pageLayout
    firstMeasure = s[music21.stream.Measure][0]
    if firstMeasure[music21.layout.PageLayout]:
        pl = firstMeasure[music21.layout.PageLayout][0]
        firstMeasure.remove(pl)
        firstMeasure.informSites()

    # check for pickup measure
    secondMeasure = s[music21.stream.Measure][1]
    if secondMeasure.quarterLength > firstMeasure.quarterLength:
        songHasPickupMeasure = True
    else:
        songHasPickupMeasure = False

    # renumber measure
    for i, measure in enumerate(s[music21.stream.Measure]):
        if songHasPickupMeasure:
            measureNumber = i
        else:
            measureNumber = i + 1

        measure.number = measureNumber
        measure.informSites()

        return song

if __name__ == '__main__':

    dirBooks = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/realbooks/"
    dirSongs = "/Users/jvo/Documents/music-visualisation/output/output-standards-ultime/"

    lines = glob.glob(dirBooks + '*' + '.mxl')
    lines = [os.path.basename(line) for line in lines]
    lines.sort()

    for line in lines[-1:]:

        print(line)

        line = line.rstrip('\n')

        book = music21.converter.parse(dirBooks + line)

        songs = separateBookIntoSongs(book)

        for song in songs:
            print(song.metadata.title)
            song = cleanSong(song)
            song.write("musicxml", dirSongs + f"{song.metadata.title}.mxl")







