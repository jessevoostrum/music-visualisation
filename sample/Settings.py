import json

from types import SimpleNamespace
import music21

class FontSettings:

    def __init__(self, settings):
        self.settings = settings

class Settings:

    def __init__(self, streamObj, settings):
        self.streamObj = streamObj
        self.settings = settings

        # self.font_settings = FontSettings(settings['fontSettings'])

        self.measuresPerLine = settings['measuresPerLine']
        self.offsetLineMax = settings['offsetLineMax']
        self.subdivision = settings['subdivision']
        self.fontSizeNotes = settings['fontSizeNotes']
        self.fontSizeGraceNotesPerFontSizeNotes = settings['fontSizeGraceNotesPerFontSizeNotes']
        self.fontSizeMetadata = settings['fontSizeMetadata']
        self.barSpacePerFontSize = settings['barSpacePerFontSize']
        self.overlapFactor = settings['overlapFactor']
        self.chordToneRatio = settings['chordToneRatio']
        self.fontSizeChordsPerFontSizeNotes = settings['fontSizeChordsPerFontSizeNotes']
        self.widthA4 = settings['widthA4']
        self.heightA4 = settings['heightA4']
        self.widthMarginLine = settings['widthMarginLine']
        self.xMinimalPickupMeasureSpaceFraction = settings['xMinimalPickupMeasureSpaceFraction']
        self.vMarginLineTop = settings['vMarginLineTop']
        self.vMarginFirstLineTop = settings['vMarginFirstLineTop']
        self.vMarginBottomMinimal = settings['vMarginBottomMinimal']
        self.alpha = settings['alpha']
        self.facecolor = settings['facecolor']
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

        f = open('sample/fontDimensions.json')
        fontDimensions = json.load(f)

        self.capsizeNumberRelative = fontDimensions[self.font]["capsize"]
        self.widthNumberRelative = fontDimensions[self.font]["width"]
        self.capsizeNumberNote = fontDimensions[self.font]["capsize"] * self.fontSizeNotes
        self.widthNumberNote = fontDimensions[self.font]["width"] * self.fontSizeNotes

        self.fontSizeNoteAccidental = self.fontSizeAccidentalRelative * self.fontSizeNotes
        self.barSpace = self.barSpacePerFontSize * self.fontSizeNotes
        self.fontSizeChords = self.fontSizeChordsPerFontSizeNotes * self.fontSizeNotes
        self.fontSizeGraceNotes = self.fontSizeGraceNotesPerFontSizeNotes * self.fontSizeNotes
        self.xMinimalPickupMeasureSpace = self.xMinimalPickupMeasureSpaceFraction * self.offsetLineMax
        self.fontSizeSegno = self.capsizeNumberRelative / fontDimensions["segno"] * self.fontSizeNotes
        self.fontSizeCoda = self.capsizeNumberRelative / fontDimensions["coda"] * self.fontSizeNotes
        self.heightBarline0Extension = self.capsizeNumberNote
        self.lengthFirstMeasure = self._getLengthFirstMeasure()
        self.offsetLineMax = self.lengthFirstMeasure * self.measuresPerLine
        self.noteLowest, self.noteHighest = self._getRangeNotes()
        self.yMin, self.yMax = self._getRangeYs()
        self.key = self._getKey()


    def getSettings(self):
        return self.settings


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
            yMin = - self.chordToneRatio * self.barSpace
        else:
            yMin = - self.barSpace * .2  # why?
        return yMin, yMax

    def _getKey(self):
        if self.streamObj[music21.key.Key].first():
            key = self.streamObj[music21.key.Key].first()
        elif self.streamObj[music21.key.KeySignature].first():
            key1 = self.streamObj[music21.key.KeySignature].first().asKey()
            if self.setInMajorKey:
                key = key1
            else:
                try:
                    key = self.streamObj.analyze('key')
                except:
                    key = music21.key.Key('C')
                    print('key analysis failed')
                if not (key == key1 or key == key1.relative):
                    print("analysed key does not correspond to keysignature")
        else:
            try:
                key = self.streamObj.analyze('key')
            except:
                key = music21.key.Key('C')
                print('key analysis failed')
            print("no key signature found")

        if self.setInMajorKey and key.mode == 'minor':
            key = key.relative

        return key


    def _getLengthFirstMeasure(self):
        length = self.streamObj.measure(1)[music21.stream.Measure][0].quarterLength
        return length