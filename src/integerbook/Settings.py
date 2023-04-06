import json
import os

import music21


class Settings:

    def __init__(self, streamObj, userSettings):

        pathSettings = os.path.join(os.path.dirname(__file__), 'settings.json')
        f = open(pathSettings)
        settings = json.load(f)

        if userSettings:
            settings.update(userSettings)

        self.streamObj = streamObj
        self.settings = settings

        self.measuresPerLine = settings['measuresPerLine']
        self.subdivision = settings['subdivision']
        self.fontSizeNotes = settings['fontSizeNotes']
        self.fontSizeGraceNotesPerFontSizeNotes = settings['fontSizeGraceNotesPerFontSizeNotes']
        self.fontSizeMetadata = settings['fontSizeMetadata']
        self.fontSizeLyrics = settings['fontSizeLyrics']
        self.fontSizeChordsPerFontSizeNotes = settings['fontSizeChordsPerFontSizeNotes']
        self.barSpacePerCapsize = settings['barSpacePerCapsize']
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
        self.yPosArranger = settings['yPosArranger']
        self.lineWidth0 = settings['lineWidth0']
        self.lineWidth1 = settings['lineWidth1']
        self.lineWidth2 = settings['lineWidth2']
        self.xMarginNote = settings['xMarginNote']
        self.font = settings['font']
        self.saveCropped = settings["saveCropped"]
        self.xkcd = settings["xkcd"]
        self.heightChordAddition = settings["heightChordAddition"]
        self.plotMelody = settings["plotMelody"]
        self.plotChordTones = settings["plotChordTones"]

        self.plotTimeSignature = settings["plotTimeSignature"]

        self.widthThickBarline = settings['widthThickBarline']
        self.timeSignatureWithBarlines = settings['timeSignatureWithBarlines']
        self.lyrics = settings['lyrics']
        self.thickBarlines = settings['thickBarlines']
        self.printArranger = settings['printArranger']
        self.xMarginNoteThickBarline = self.widthThickBarline - 0.5 * self.lineWidth0
        self.usePlt = settings["usePlt"]
        self.vMarginLyricsRelative = settings["vMarginLyricsRelative"]


        # Font stuff

        self.fontSettings = FontSettings(self.font)

        self.fontDirectory = settings['fontDirectory']
        self.fontPath = settings["fontPath"]
        self.fontPathRoman = settings["fontPathRoman"]
        self.fontStyle = settings["fontStyle"]
        self.fontWeight = settings["fontWeight"]
        self.fontSizeAccidentalRelative = settings['fontSizeAccidentalRelative']


        pathFontDimensions = os.path.join(os.path.dirname(__file__), 'fontDimensions.json')
        f = open(pathFontDimensions)
        fontDimensions = json.load(f)
        if self.font in fontDimensions:
            fD = fontDimensions[self.font]
        else:
            fD = fontDimensions["DejaVu Sans"]
            print("no font dimensions available")

        fDLyrics = fontDimensions["DejaVu Sans"]

        self.capsizeNumberRelative = fD["capsize"]
        self.widthNumberRelative = fD["width"]
        if "vShift" in fD.keys():
            self.fontVShift = fD["vShift"]
        else:
            self.fontVShift = None

        self.capsizeNote = fD["capsize"] * self.fontSizeNotes
        self.fontWidthNote = fD["width"] * self.fontSizeNotes

        self.fontSizeChords = self.fontSizeChordsPerFontSizeNotes * self.fontSizeNotes
        self.capsizeChord = fD["capsize"] * self.fontSizeChords
        self.fontWidthChord = fD["width"] * self.fontSizeChords

        self.capsizeLyric = fDLyrics["capsize"] * self.fontSizeLyrics
        self.fontWidthLyric = fDLyrics["width"] * self.fontSizeLyrics

        self.capsizeType = fD["capsize"] * self.fontSettings.fontSizeType

        self.fontSizeSegno = self.capsizeNumberRelative / fontDimensions["segno"] * self.fontSizeNotes
        self.fontSizeCoda = self.capsizeNumberRelative / fontDimensions["coda"] * self.fontSizeNotes
        self.lyricHeightMax = self._countLinesLyrics() * self.capsizeLyric * (1 + self.vMarginLyricsRelative) + self.capsizeLyric * self.vMarginLyricsRelative

        self.fontSizeNoteAccidental = self.fontSizeAccidentalRelative * self.fontSizeNotes
        self.barSpace = self.barSpacePerCapsize * self.capsizeNote
        self.fontSizeChords = self.fontSizeChordsPerFontSizeNotes * self.fontSizeNotes
        self.fontSizeGraceNotes = self.fontSizeGraceNotesPerFontSizeNotes * self.fontSizeNotes

        self.heightBarline0Extension = self.capsizeNote
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
        yMin = 0

        chords = len(self.streamObj.flatten().getElementsByClass('ChordSymbol')) > 0
        if chords:
            yMin -= max(self.heightChordAddition * self.capsizeChord + self.capsizeType, self.capsizeType)

        if self.lyrics:
            yMin -= self.lyricHeightMax
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

class FontSettings:

    def __init__(self, font):

        pathFontDimensions = os.path.join(os.path.dirname(__file__), 'fontSettings.json')
        f = open(pathFontDimensions)
        fontSettings = json.load(f)
        if font in fontSettings.keys():
            fontSettings = fontSettings[font]
        else:
            fontSettings = fontSettings['DejaVu Sans']
            print("no fontsettings available")

        self.fontSizeType = fontSettings['fontSizeType']
        self.fontSizeTypeSmall = fontSettings['fontSizeTypeSmall']
        self.widthCharacter = fontSettings['widthCharacter']
        self.widthMinus = fontSettings['widthMinus']
        self.accidentalSpace = fontSettings['accidentalSpace']
        self.accidentalSizeRelative = fontSettings["accidentalSizeRelative"]
        self.widthDelta = fontSettings["widthDelta"]
        self.widthCircle = fontSettings["widthCircle"]
        self.spaceAddSus = fontSettings["spaceAddSus"]
        self.accidentalXPositionRelative = fontSettings["accidentalXPositionRelative"]
        self.hDistanceChordAddition = fontSettings['hDistanceChordAddition']
