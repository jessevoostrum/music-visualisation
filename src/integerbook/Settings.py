import json
import os

import music21
from integerbook.FontSettings import FontSettings


class Settings:

    def __init__(self, userSettings):

        pathSettings = os.path.join(os.path.dirname(__file__), 'settings.json')
        f = open(pathSettings)
        settings = json.load(f)

        settings.update(userSettings)

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
        self.widthA4 = settings['widthA4']
        self.heightA4 = settings['heightA4']
        self.widthMarginLine = settings['widthMarginLine']
        self.xMinimalPickupMeasureSpaceFraction = settings['xMinimalPickupMeasureSpaceFraction']
        self.vMarginLineTop = settings['vMarginLineTop']
        self.vMarginFirstLineTop = settings['vMarginFirstLineTop']
        self.vMarginBottomMinimal = settings['vMarginBottomMinimal']

        self.facecolorMelody = settings['facecolorMelody']
        self.facecolorSecondVoice = settings["facecolorSecondVoice"]
        self.facecolorChordNotes = settings['facecolorChordNotes']
        self.colorTextMelody = settings["colorTextMelody"]
        self.colorTextChords = settings["colorTextChords"]
        self.colorTextChordNotes = settings["colorTextChordNotes"]
        self.colorLyrics = settings["colorLyrics"]
        self.colorTextKey = settings["colorTextKey"]
        self.colorBarlines = settings["colorBarlines"]
        self.alphaMelody = settings['alphaMelody']
        self.alphaChordNotes = settings["alphaChordNotes"]

        self.coloringCircleOfFifths = settings['coloringCircleOfFifths']
        self.coloringVoices = settings['coloringVoices']

        self.ptToInches = settings['ptToInches']
        self.capHeightRatio = settings['capHeightRatio']
        self.xShiftNumberNote = settings['xShiftNumberNote']
        self.xShiftChords = settings['xShiftChords']
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
        self.plotChordNotes = settings["plotChordNotes"]

        self.plotTimeSignature = settings["plotTimeSignature"]

        self.widthThickBarline = settings['widthThickBarline']
        self.timeSignatureWithBarlines = settings['timeSignatureWithBarlines']

        self.plotLyrics = settings['plotLyrics']
        self.plotBarlines = settings["plotBarlines"]
        self.plotMetadata = settings["plotMetadata"]
        self.plotChords = settings["plotChords"]

        self.thickBarlines = settings['thickBarlines']
        self.extendBarlineTop = settings["extendBarlineTop"]
        self.printArranger = settings['printArranger']
        self.vMarginLyricsRelative = settings["vMarginLyricsRelative"]
        self.alternativeSymbols = settings["alternativeSymbols"]
        self.chordVerbosity = settings["chordVerbosity"]

        self.forceMinor = settings["forceMinor"]

        self.minorFromParallelMajorScalePerspective = settings["minorFromParallelMajorScalePerspective"]
        self.minorFromRelativeMajorScalePerspective = settings['minorFromRelativeMajorScalePerspective']
        self.minorFromMinorScalePerspective = settings["minorFromMinorScalePerspective"]



        self.romanNumerals = settings["romanNumerals"]
        self.numbersRelativeToChord = settings["numbersRelativeToChord"]
        self.manualSecondaryChords = settings["manualSecondaryChords"]

        self.plotFirstKeyWithinBar = settings["plotFirstKeyWithinBar"]

        self.dpi = settings["dpi"]
        self.outputFormat = settings["outputFormat"]

        self.fontDirectory = settings['fontDirectory']
        self.fontPath = settings["fontPath"]
        self.fontPathRoman = settings["fontPathRoman"]
        self.fontStyle = settings["fontStyle"]
        self.fontWeight = settings["fontWeight"]
        self.fontSizeAccidentalRelative = settings['fontSizeAccidentalRelative']
        self.scroll = settings["scroll"]

        ### change settings

        if self.scroll:
            self.plotMetadata = False
            self.plotFirstKeyWithinBar = True

        ### check if settings are passed correctly

        if self.minorFromParallelMajorScalePerspective + self.minorFromRelativeMajorScalePerspective + self.minorFromMinorScalePerspective != 1:
            print("specify minor scale perspecive")

        if self.coloringVoices + self.coloringCircleOfFifths != 1:
            print('specify coloring scheme')

        ###

        self.xyRatio = self.widthA4 / self.heightA4
        self.xMarginNoteThickBarline = self.widthThickBarline - 0.5 * self.lineWidth0

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
        self.fontSizeSecondaryChord = self.settings["fontSizeSecondaryChordPerFontSizeChord"] * self.fontSizeChords
        self.capsizeChord = fD["capsize"] * self.fontSizeChords
        self.capsizeSecondaryChord = fD["capsize"] * self.fontSizeSecondaryChord
        self.fontWidthChord = fD["width"] * self.fontSizeChords

        self.capsizeLyric = fDLyrics["capsize"] * self.fontSizeLyrics
        self.fontWidthLyric = fDLyrics["width"] * self.fontSizeLyrics

        self.fontSizeType = settings['fontSizeTypePerFontSizeChord'] * self.fontSizeChords
        self.fontSizeTypeSecondaryChord = settings['fontSizeTypePerFontSizeChord'] * self.fontSizeSecondaryChord

        self.fontSettings = FontSettings(self.font, self.fontSizeType)

        self.capsizeType = fD["capsize"] * self.fontSizeType

        self.fontSizeNoteAccidental = self.fontSizeAccidentalRelative * self.fontSizeNotes
        self.barSpace = self.barSpacePerCapsize * self.capsizeNote
        self.fontSizeChords = self.fontSizeChordsPerFontSizeNotes * self.fontSizeNotes
        self.fontSizeGraceNotes = self.fontSizeGraceNotesPerFontSizeNotes * self.fontSizeNotes

        if self.extendBarlineTop:
            self.heightBarline0Extension = self.capsizeNote
        else:
            self.heightBarline0Extension = 0

        self.lineHeightLyrics = (1 + self.vMarginLyricsRelative) * self.capsizeLyric




    def updateSettings(self, streamObj):
        
        self.numLinesLyrics = self._countNumLinesLyrics(streamObj)

        self.lyricHeightMax = self._countNumVoices(streamObj) * self.numLinesLyrics * self.lineHeightLyrics + self.capsizeLyric * self.vMarginLyricsRelative

        self.lengthFirstMeasure = self._getLengthFirstMeasure(streamObj)
        self.offsetLineMax = self.lengthFirstMeasure * self.measuresPerLine
        self.xMinimalPickupMeasureSpace = self.xMinimalPickupMeasureSpaceFraction * self.offsetLineMax
        self.noteLowest, self.noteHighest = self._getRangeNotes(streamObj)
        self.yMin, self.yMax = self._getRangeYs(streamObj)



    def _getRangeNotes(self, streamObj):
        if self.plotMelody:
            p = music21.analysis.discrete.Ambitus()
            if p.getPitchSpan(streamObj):
                pitchSpan = [int(thisPitch.ps) for thisPitch in p.getPitchSpan(streamObj)]
                return pitchSpan[0], pitchSpan[1]
            else:
                return 1, 10
        else:
            nL = int(self.getKey(0).getTonic().ps)
            nH = nL + 12
            return nL, nH

    def _getRangeYs(self, streamObj):
        numTones = self.noteHighest - self.noteLowest + 1
        yMax = numTones * self.barSpace * (1 - self.overlapFactor) + self.barSpace * self.overlapFactor
        yMin = 0

        chords = len(streamObj.flatten().getElementsByClass('ChordSymbol')) > 0
        if chords and self.plotChords:
            yMin -= max(self.heightChordAddition * self.capsizeChord + self.capsizeType, self.capsizeType)

        if self.plotLyrics:
            yMin -= self.lyricHeightMax  # ? this is zero when there are no lyrics
        return yMin, yMax

    def _countNumVoices(self, streamObj):
        "maximum is 2"
        for el in streamObj[music21.note.Note]:
            if el.containerHierarchy():
                container = el.containerHierarchy()[0]
                if type(container) == music21.stream.Voice:
                    if container.id == '2':
                        return 2
        return 1

    def _countNumLinesLyrics(self, streamObj):
        maxNumLines = 0
        for el in streamObj[music21.note.Note]:
            if el.lyric:
                numLines = el.lyric.count('\n') + 1
                if numLines > maxNumLines:
                    maxNumLines = numLines

        return maxNumLines


    def _getLengthFirstMeasure(self, streamObj):
        length = streamObj.measure(1)[music21.stream.Measure][0].quarterLength
        return length




