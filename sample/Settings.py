import json

from types import SimpleNamespace
import music21

from sample.plotter.Plotter import Plotter


# class FontSettings:
#
#     def __init__(self, settings):
#         self.settings = settings

class Settings:

    def __init__(self, streamObj, settings):
        self.streamObj = streamObj
        self.settings = settings

        # self.font_settings = FontSettings(settings['fontSettings'])

        self.measuresPerLine = settings['measuresPerLine']
        self.subdivision = settings['subdivision']
        self.fontSizeNotes = settings['fontSizeNotes']
        self.fontSizeGraceNotesPerFontSizeNotes = settings['fontSizeGraceNotesPerFontSizeNotes']
        self.fontSizeMetadata = settings['fontSizeMetadata']
        self.fontSizeLyrics = settings['fontSizeLyrics']
        self.fontSizeChordsPerFontSizeNotes = settings['fontSizeChordsPerFontSizeNotes']
        self.barSpacePerFontSize = settings['barSpacePerFontSize']
        self.overlapFactor = settings['overlapFactor']
        self.chordToneRatio = settings['chordToneRatio']
        self.widthA4 = settings['widthA4']
        self.heightA4 = settings['heightA4']
        self.widthMarginLine = settings['widthMarginLine']
        self.xMinimalPickupMeasureSpaceFraction = settings['xMinimalPickupMeasureSpaceFraction']
        self.vMarginLineTop = settings['vMarginLineTop']
        self.vMarginFirstLineTop = settings['vMarginFirstLineTop']
        self.vMarginBottomMinimal = settings['vMarginBottomMinimal']
        self.alpha = settings['alpha']
        self.coloursCircleOfFifths = settings['coloursCircleOfFifths']
        self.coloursVoices = settings['coloursVoices']
        self.ptToInches = settings['ptToInches']
        self.capHeightRatio = settings['capHeightRatio']
        self.xShiftNumberNote = settings['xShiftNumberNote']
        self.xShiftChords = settings['xShiftChords']
        self.setInMajorKey = settings['setInMajorKey']
        self.yLengthTitleAx = settings['yLengthTitleAx']
        self.yPosTitle = settings['yPosTitle']
        self.yPosComposer = settings['yPosComposer']
        self.yPosPlayer = settings['yPosPlayer']
        self.lineWidth0 = settings['lineWidth0']
        self.lineWidth1 = settings['lineWidth1']
        self.lineWidth2 = settings['lineWidth2']
        self.xMarginNote = settings['xMarginNote']
        self.radiusCorners = settings['radiusCorners']
        self.mutationAspect = settings['mutationAspect']
        self.font = settings['font']
        self.fontSizeAccidentalRelative = settings['fontSizeAccidentalRelative']
        self.hDistanceChordAddition = settings['hDistanceChordAddition']
        self.widthThickBarline = settings['widthThickBarline']
        self.timeSignatureWithBarlines = settings['timeSignatureWithBarlines']
        self.lyrics = settings['lyrics']
        self.thickBarlines = settings['thickBarlines']

        f = open('sample/fontDimensions.json')
        fontDimensions = json.load(f)

        self.capsizeNumberRelative = fontDimensions[self.font]["capsize"]
        self.widthNumberRelative = fontDimensions[self.font]["width"]
        self.capsizeNumberNote = fontDimensions[self.font]["capsize"] * self.fontSizeNotes
        self.widthNumberNote = fontDimensions[self.font]["width"] * self.fontSizeNotes
        self.fontSizeSegno = self.capsizeNumberRelative / fontDimensions["segno"] * self.fontSizeNotes
        self.fontSizeCoda = self.capsizeNumberRelative / fontDimensions["coda"] * self.fontSizeNotes
        self.lyricHeightMax = fontDimensions["firstLineHeight"] * self.fontSizeLyrics + (self._countLinesLyrics() - 1) * fontDimensions["extraLineHeight"] * self.fontSizeLyrics

        self.fontSizeNoteAccidental = self.fontSizeAccidentalRelative * self.fontSizeNotes
        self.barSpace = self.barSpacePerFontSize * self.fontSizeNotes
        self.fontSizeChords = self.fontSizeChordsPerFontSizeNotes * self.fontSizeNotes
        self.fontSizeGraceNotes = self.fontSizeGraceNotesPerFontSizeNotes * self.fontSizeNotes

        self.heightBarline0Extension = self.capsizeNumberNote
        self.lengthFirstMeasure = self._getLengthFirstMeasure()
        self.offsetLineMax = self.lengthFirstMeasure * self.measuresPerLine
        self.xMinimalPickupMeasureSpace = self.xMinimalPickupMeasureSpaceFraction * self.offsetLineMax
        self.noteLowest, self.noteHighest = self._getRangeNotes()
        self.yMin, self.yMax = self._getRangeYs()

        key = self.getKey(0)
        if key.mode == 'major':
            self.facecolor = settings['facecolor']
            self.facecolor2 = settings['facecolor2']

        else:
            self.facecolor = settings['facecolor2']
            self.facecolor2 = settings['facecolor']


    def getSettings(self):
        return self.settings

    def getKey(self, offset):
        lastKey = None
        if self.streamObj[music21.key.Key, music21.key.KeySignature]:
            for key in self.streamObj[music21.key.Key, music21.key.KeySignature]:
                offsetKey = key.getOffsetInHierarchy(self.streamObj)
                key = self._preprocessKey(key)
                if offset >= offsetKey:
                    lastKey = key
                else:
                    break

        if not lastKey:
            print('no key signature')
            try:
                lastKey = self.streamObj.analyze('key')
            except:
                lastKey = music21.key.Key('C')
                print('key analysis failed')

        return lastKey

    def _preprocessKey(self, key):
        if type(key) == music21.key.KeySignature:
            key = key.asKey()

        if self.setInMajorKey and key.mode == 'minor':
            key = key.relative

        return key


    def _getRangeNotes(self):
        p = music21.analysis.discrete.Ambitus()
        if p.getPitchSpan(self.streamObj):
            pitchSpan = [int(thisPitch.ps) for thisPitch in p.getPitchSpan(self.streamObj)]
            return pitchSpan[0], pitchSpan[1]
        else:
            return 1, 10

    def _getRangeYs(self):
        numTones = self.noteHighest - self.noteLowest + 1
        yMax = numTones * self.barSpace * (1 - self.overlapFactor) + self.barSpace * self.overlapFactor
        chords = len(self.streamObj.flat.getElementsByClass('Chord')) > 0
        if chords:
            chordHeight = self.fontSizeChordsPerFontSizeNotes * self.capsizeNumberNote * 1.3
            yMarginTopChord = self.fontSizeChords * 1
            if self.lyrics:
                yMin = - (chordHeight + self.lyricHeightMax)
            else:
                yMin = - self.chordToneRatio * self.barSpace
        else:
            yMin = - self.barSpace * .2  # why?
        return yMin, yMax

    def _countLinesLyrics(self):
        maxNumLines = 0
        for el in self.streamObj[music21.note.Note]:
            if el.lyric:
                numLines = el.lyric.count('\n') + 1
                if numLines > maxNumLines:
                    maxNumLines = numLines

        return maxNumLines


    def _getLengthFirstMeasure(self):
        length = self.streamObj.measure(1)[music21.stream.Measure][0].quarterLength
        return length