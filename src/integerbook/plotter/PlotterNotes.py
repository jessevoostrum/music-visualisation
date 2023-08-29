import os
import json
import io
import music21
from matplotlib.backend_bases import RendererBase
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse
from itertools import tee, islice, chain
import numpy as np

from integerbook.plotter.patches import Parallelogram
from integerbook.plotter.PlotterBase import Plotter

from integerbook.plotter.PlotterChords import PlotterChords


class PlotterNotes(Plotter):

    def __init__(self, streamObj, Settings, LocationFinder, axs,):

        super().__init__(streamObj, Settings, LocationFinder, axs)

        self.barSpace = Settings.barSpace
        self.noteLowest = Settings.noteLowest

        self.graceNoteCounter = 0

        # for plotting lyrics

        self.xPosLyricEnd = {"1": 0,
                             "2": 0,
                             "3": 0,
                             "4": 0}
        self.yPosLineBaseLast = {"1": 0,
                                 "2": 0,
                                 "3": 0,
                                 "4": 0}
        self.lastSyllabic = {"1": 0,
                             "2": 0,
                             "3": 0,
                             "4": 0}

        if self.Settings.alternativeSymbols:
            pathAlternativeSymbols = os.path.join(os.path.dirname(__file__), '../alternativeSymbols.json')
            f = open(pathAlternativeSymbols)
            self.alternativeSymbolsDict = json.load(f)[self.Settings.alternativeSymbols]

        if self.Settings.numbersRelativeToChord:
            self.chordList = self._makeChordList()

    def plotNotes(self):

        notes = self.streamObj[music21.note.Note]
        chords = self.streamObj[music21.chord.Chord]

        for idx in range(len(notes)):

            note = notes[idx]
            if idx < len(notes) - 1:
                noteNext = notes[idx + 1]
            else:
                noteNext = None

            measure = note.containerHierarchy()[0]
            offset = note.getOffsetInHierarchy(self.streamObj)
            self._plotNote(note, noteNext, measure, offset)

        for chord in chords:
            if type(chord) == music21.chord.Chord:
                measure = chord.containerHierarchy()[0]
                for note in chord.notes:
                    noteNext = None
                    self._plotNote(note, noteNext, measure, offset=chord.getOffsetInHierarchy(self.streamObj))

    def plotChordNotes(self):

        chords = self.streamObj[music21.harmony.ChordSymbol]

        nL = self.Settings.noteLowest
        nH = self.Settings.noteHighest

        for idx in range(len(chords)):

            chord = chords[idx]

            if idx < len(chords) - 1:
                chordNext = chords[idx+1]
            else:
                chordNext = None

            offset = chord.getOffsetInHierarchy(self.streamObj)
            measure = chord.containerHierarchy()[0]
            if chordNext:
                offsetNext = chordNext.getOffsetInHierarchy(self.streamObj)
                measureNext = chordNext.containerHierarchy()[0]
                measureEnd = self._getMeasureByNumber(measureNext.number-1)
            else:
                offsetNext = self.streamObj.quarterLength
                measureEnd = self.streamObj[music21.stream.Measure][-1]

            notes = chord.notes
            for note in notes:
                midiNumber = note.pitch.ps

                midiNumberPlottedNote = nL + (midiNumber - nL) % 12
                while midiNumberPlottedNote <= nH:
                    plottedNote = music21.note.Note(midiNumberPlottedNote, quarterLength=offsetNext - offset)
                    self._plotNote(plottedNote, None, measure, offset=offset, measureEnd=measureEnd, isChordNote=True)
                    midiNumberPlottedNote += 12

    def _plotNote(self, el, elNext, measure,  offset, measureEnd=None, isChordNote=False):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)
        yPosWithinLine = self._yPosWithinLine(el)
        yPos = yPosLineBase + yPosWithinLine
        offsetLength = el.duration.quarterLength
        xLength = self.LocationFinder._getXLengthFromOffsetLength(offsetLength)

        key = self.Settings.getKey(offset)

        slope = None
        if self._isGlissando(el):
            slope = self._plotParallelogram(page, el, xPos, xLength,  yPos, yPosLineBase, key, measure, offset)
        elif not self._isGraceNote(el):
            self._plotRectangle(page, el, xPos, xLength,  yPos, key, measure, offset, measureEnd,  isChordNote=isChordNote)

        self._plotNumber(page, el, elNext, xPos, xLength, yPos, slope, key, offset, isChordNote=isChordNote)

        self._plotArticulation(el, elNext)

        if self.Settings.lyrics:
            self._plotLyric(page, el, xPos, yPosLineBase)

    def _plotRectangle(self, page, el, xPos, xLength,  yPos, key, measure, offset, measureEnd=None, isChordNote=False):

        if not measureEnd:
            measureEnd = measure

        if not el.tie:
            shape = 'rounded'
            if not self._overlapStartWithThickBarline(el, offset, measure):
                xPos += self.Settings.xMarginNote
                xLength -= self.Settings.xMarginNote
            else:
                xPos += self.Settings.xMarginNoteThickBarline  # for info see position of thick barline
                xLength -= self.Settings.xMarginNoteThickBarline
            if not self._overlapEndWithThickBarline(el, offset, measureEnd):
                xLength -= self.Settings.xMarginNote
            else:
                xLength -= self.Settings.xMarginNoteThickBarline

        else:
            if el.tie.type == 'start':
                shape = 'leftRounded'
                if not self._overlapStartWithThickBarline(el, offset, measure):
                    xPos += self.Settings.xMarginNote
                    xLength -= self.Settings.xMarginNote
                else:
                    xPos += self.Settings.xMarginNoteThickBarline
                    xLength -= self.Settings.xMarginNoteThickBarline
            elif el.tie.type == 'continue':
                shape = 'straight'
            else:
                shape = 'rightRounded'
                if not self._overlapEndWithThickBarline(el, offset, measureEnd):
                    xLength -= self.Settings.xMarginNote
                else:
                    xLength -= self.Settings.xMarginNoteThickBarline

        if self._isVibrato(el):
            shape = 'squiggly'

        alpha, facecolor, hatch = self._adjustVisualParameters(el, key, isChordNote)

        leftBottom = [xPos, yPos]
        leftTop = [xPos, yPos + self.barSpace]
        rightBottom = [xPos + xLength, yPos]
        rightTop = [xPos + xLength, yPos + self.barSpace]

        patch = Parallelogram(leftBottom, leftTop, rightBottom, rightTop, alpha, facecolor, hatch, shape=shape)

        self.axs[page].add_patch(patch)

    def _plotParallelogram(self, page, el, xPos, xLength,  yPos, yPosLineBase, key, measure, offset):

        sp = el.getSpannerSites()[0]
        alpha, facecolor, hatch = self._adjustVisualParameters(el, key)

        if self._isStartGlissando(el):
            noteTarget = sp.getLast()

            yTarget = self._yPosWithinLine(noteTarget) + yPosLineBase
            yMiddle = (yTarget + yPos) / 2

            if not self._overlapStartWithThickBarline(el, offset, measure):
                xPos += self.Settings.xMarginNote
                xLength -= self.Settings.xMarginNote
            else:
                xPos += self.Settings.xMarginNoteThickBarline
                xLength -= self.Settings.xMarginNoteThickBarline

            leftBottom = [xPos, yPos]
            leftTop = [xPos, yPos + self.barSpace]
            rightBottom = [xPos + xLength, yMiddle]
            rightTop = [xPos + xLength, yMiddle + self.barSpace]

            shape = 'leftRounded'

        else:
            noteOrigin = sp.getFirst()
            yOrigin = self._yPosWithinLine(noteOrigin) + yPosLineBase

            yMiddle = (yOrigin + yPos) / 2

            if not self._overlapEndWithThickBarline(el, offset, measure):
                xLength -= self.Settings.xMarginNote
            else:
                xLength -= self.Settings.xMarginNoteThickBarline

            leftBottom = [xPos, yMiddle]
            leftTop = [xPos, yMiddle + self.barSpace]
            rightBottom = [xPos + xLength, yPos]
            rightTop = [xPos + xLength, yPos + self.barSpace]

            shape = 'rightRounded'

        patch = Parallelogram(leftBottom, leftTop, rightBottom, rightTop, alpha, facecolor, hatch, shape=shape)
        self.axs[page].add_patch(patch)

        slope = (rightBottom[1] - leftBottom[1]) / xLength
        return slope

    def _plotNumber(self, page, el, elNext, xPos, xLength, yPos, slope, key, offset, isChordNote=False):
        if not (el.tie and not (el.tie.type == 'start')):
            number, accidental = key.getScaleDegreeAndAccidentalFromPitch(el.pitch)

            if self.Settings.numbersRelativeToChord:
                number, accidental = self._getNumberRelativeToChord(el, offset, accidental)

            if not self._isGraceNote(el):
                xShiftNumbers = self._computeXShiftNumbers(el, xLength)
                fontSize = self.Settings.fontSizeNotes
            else:
                xShiftNumbers = self._computeXShiftNumbersGraceNote(el, elNext)
                fontSize = self.Settings.fontSizeGraceNotes

            horizontalAlignment = 'left'

            if not self._isGlissando(el):
                xPos += xShiftNumbers

            else:
                xShiftNumbersGlissando = 0.002
                if self._isStartGlissando(el):
                    yPos += slope * (xShiftNumbersGlissando + self.Settings.fontWidthNote / 2)
                    xPos += xShiftNumbersGlissando

                elif self._isEndGlissando(el):
                    xPos += xLength
                    xPos -= xShiftNumbersGlissando
                    yPos -= slope * (xShiftNumbersGlissando + self.Settings.fontWidthNote / 2)
                    horizontalAlignment = 'right'

            yPos += self._computeYShiftNumbers()

            textColor = 'black'
            alpha = 1
            zorder = 1
            if isChordNote:
                textColor = 'grey'
                alpha = 0.5
                zorder = .5

            if not self.Settings.alternativeSymbols:
                self.axs[page].text(xPos, yPos, number,
                                    fontsize=fontSize,
                                    va='baseline', ha=horizontalAlignment, color=textColor, zorder=zorder)


                self._plotAccidental(accidental, fontSize, xPos, yPos, page)

            else:
                symbol = self._getSymbol(number, accidental)
                self.axs[page].text(xPos, yPos, symbol,
                                    fontsize=fontSize,
                                    va='baseline', ha=horizontalAlignment, color=textColor, zorder=zorder)

    def _plotLyric(self, page, el, xPos, yPosLineBase):
        """lyrics are plotted with vertical_alignment='top' at yPosLineBass.
        By multiple lines, the lyric already contains a newline command within it"""

        if el.lyrics:
            for lyric in el.lyrics:

                marginTop = self.Settings.vMarginLyricsRelative
                lineNumber = lyric.number
                strLineNumber = str(lineNumber)

                xPosLyric = xPos + self.Settings.xShiftNumberNote / 4
                sameLineAsLastElement = self.yPosLineBaseLast[strLineNumber] == yPosLineBase

                if xPosLyric < self.xPosLyricEnd[strLineNumber] and sameLineAsLastElement:
                    xPosLyric = self.xPosLyricEnd[strLineNumber] + self.Settings.fontWidthLyric * 0.3

                yPos = yPosLineBase - lineNumber * (1 + marginTop) * self.Settings.capsizeLyric

                plottedLyric = self.axs[page].text(xPosLyric, yPos, lyric.text,
                                                   fontsize=self.Settings.fontSizeLyrics,
                                                   va='baseline', ha='left', font='Dejavu Sans', fontstyle='normal')

                renderer = self.axs[page].figure._get_renderer()
                bb = plottedLyric.get_window_extent(renderer=renderer).transformed(self.axs[page].transData.inverted())
                lyricWidth = bb.width

                if self.lastSyllabic[strLineNumber] == 'middle' or self.lastSyllabic[strLineNumber] == 'begin':
                    """note that in musescore export there is often middle and end syllable, after middle there is a hyphen"""

                    if sameLineAsLastElement:
                        xPosHyphen = (self.xPosLyricEnd[strLineNumber] + xPosLyric) / 2
                    else:
                        xPosHyphen = self.xPosLyricEnd[strLineNumber] + self.Settings.fontWidthLyric * 0.3
                        yPos = self.yPosLineBaseLast[strLineNumber] - lineNumber * (1 + marginTop) * self.Settings.capsizeLyric

                    self.axs[page].text(xPosHyphen, yPos, "-",
                                        fontsize=self.Settings.fontSizeLyrics,
                                        va='baseline', ha='center', font='Dejavu Sans', fontstyle='normal')

                self.xPosLyricEnd[strLineNumber] = xPosLyric + lyricWidth

                self.yPosLineBaseLast[strLineNumber] = yPosLineBase

                self.lastSyllabic[strLineNumber] = lyric.syllabic

    def _adjustVisualParameters(self, el, key, isChordNote=False):

        facecolor = self.Settings.facecolor
        alpha = self.Settings.alpha
        hatch = None


        if self.Settings.coloursCircleOfFifths:

            pitchKey = key.getTonic().ps
            pitchNote = el.pitch.ps
            relativePitch = (pitchNote - pitchKey) % 12
            circleOfFifthIndex = self._relativePitchToCircleOfFifthsIndex(relativePitch)

            facecolor = self._colorwheel(circleOfFifthIndex)
            alpha = self._alpha(circleOfFifthIndex)


        elif self.Settings.coloursVoices:
            if el.containerHierarchy():
                container = el.containerHierarchy()[0]
                if type(container) == music21.stream.Voice:
                    if container.id == '2':
                        facecolor = self.Settings.facecolor2

        # ghost note
        if el.notehead == 'x':
            facecolor = 'grey'
            alpha = 0.15
            hatch = 'xxxxx'  # this controls the fine graindedness of the x pattern? TODO: make notebook

        if isChordNote:
            facecolor = 'red'
            alpha=0.05

        return alpha, facecolor, hatch

    def _yPosWithinLine(self, el):
        yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.Settings.overlapFactor)
        return yPosWithinLine

    def _isGlissando(self, el):
        if el.getSpannerSites():
            sp = el.getSpannerSites()[0]
            return type(sp) == music21.spanner.Glissando
        else:
            return False

    def _isStartGlissando(self, el):
        if self._isGlissando(el):
            sp = el.getSpannerSites()[0]
            return sp.isFirst(el)
        else:
            return False

    def _isEndGlissando(self, el):
        if self._isGlissando(el):
            sp = el.getSpannerSites()[0]
            return sp.isLast(el)
        else:
            return False

    def _isGraceNote(self, el):
        return not el.duration.linked

    def _relativePitchToCircleOfFifthsIndex(self, relativePitch):
        pitchesCircleOfFifths = [(i*7) % 12 for i in range(12)]
        return pitchesCircleOfFifths.index(relativePitch)

    def _alpha(self, circleOfFifthIndex):
        lowestAlpha = 0.2
        highestAlpha = 0.4
        firstAlphas = np.linspace(lowestAlpha, highestAlpha, 6, endpoint=False)
        lastAlphas = np.linspace(highestAlpha, lowestAlpha, 6, endpoint=False)
        alphas = np.concatenate((firstAlphas, lastAlphas))
        alpha = alphas[circleOfFifthIndex]
        return alpha

    def _computeXShiftNumbers(self, el,xLength):

        xShiftNumbers = self.Settings.xShiftNumberNote
        if xLength < (2 * self.Settings.xShiftNumberNote + self.Settings.fontWidthNote) and (not el.tie):
            xShiftNumbers = 0.5 * xLength - 0.5 * self.Settings.fontWidthNote

        return xShiftNumbers

    def _computeXShiftNumbersGraceNote(self, el, elNext):

        # single grace note
        if not el.beams.beamsList:
            xShiftNumbers = 0

        # multiple grace notes
        else:
            if el.beams.getTypes()[0] == 'start':  #
                xShiftNumbers = 0
                self.graceNoteCounter += 1
            elif el.beams.getTypes()[0] == 'continue':
                if elNext.beams.getTypes()[0] == 'continue': # max of 4 grace notes supported
                    xShiftNumbers = self.Settings.xShiftNumberNote / 4
                    self.graceNoteCounter += 1
                elif elNext.beams.getTypes()[0] == 'stop':
                    xShiftNumbers = self.Settings.xShiftNumberNote * self.graceNoteCounter / (self.graceNoteCounter + 2)
                    self.graceNoteCounter += 1
            elif el.beams.getTypes()[0] == 'stop':
                xShiftNumbers = self.Settings.xShiftNumberNote * self.graceNoteCounter / (self.graceNoteCounter + 1)
                self.graceNoteCounter = 0

        return xShiftNumbers


    def _computeYShiftNumbers(self):

        yShiftNumbers = (self.barSpace - self.Settings.capsizeNote) / 2

        if self.Settings.fontVShift:
            yShiftNumbers += self.Settings.fontVShift * self.Settings.capsizeNote

        return yShiftNumbers


    def _plotArticulation(self, el, elNext):
        if elNext:
            articulation = self._getArticulation(el, elNext)
            if articulation:
                offset = el.getOffsetInHierarchy(self.streamObj)
                page, yPosLineBase, xPosStart = self.LocationFinder.getLocation(offset)

                yPosWithinLine = self._yPosWithinLine(el)
                yPos1 = yPosLineBase + yPosWithinLine
                yPosWithinLine = self._yPosWithinLine(elNext)
                yPos2 = yPosLineBase + yPosWithinLine

                yShrink = 0.1 * self.barSpace
                yPosLow = min(yPos1, yPos2) + yShrink
                yPosHigh = max(yPos1, yPos2) + self.barSpace - yShrink

                yPosCenter = (yPosLow + yPosHigh) / 2


                offsetLength = el.duration.quarterLength
                xLength = self.LocationFinder._getXLengthFromOffsetLength(offsetLength)
                xPos = xPosStart + xLength


                #self.axs[page].vlines(xPos, yPosLow, yPosHigh, alpha=.7)
                width = 2 * self.Settings.xMarginNote
                patchLine = FancyBboxPatch((xPos - width/2, yPosLow),
                                       width, yPosHigh - yPosLow,
                                       boxstyle=f"round, pad=0, rounding_size=0.002",
                                       mutation_aspect=0.15,
                                       facecolor='blue', alpha=1,
                                        linewidth=0
                                       )
                self.axs[page].add_patch(patchLine)

                fontsize = 6
                fontHeight = fontsize * 0.0008554
                height = fontHeight

                width = width * 2

                patchRectangle = Rectangle((xPos - width/2, yPosCenter - height/2), width, height, facecolor='white', zorder=2 )
                self.axs[page].add_patch(patchRectangle)

                radius = self.barSpace
                yxRatio =  self.Settings.heightA4 / self.Settings.widthA4
                patch = Ellipse((xPos, yPosCenter), width=radius * yxRatio, height=radius, facecolor='white', zorder=2, alpha=.0)

                self.axs[page].add_patch(patch)

                fontsize = 7
                fontHeight = fontsize * 0.0008554
                yPosBaseline = yPosCenter -  fontHeight / 2
                if articulation == 'hammer on':
                    letter = "H"
                else:
                    letter = "P"
                self.axs[page].text(xPos, yPosBaseline, letter, ha='center', va='baseline', font='Arial', fontsize=7, fontstyle='normal', zorder=2)



    def _getArticulation(self, el, elNext):
        articulation = None
        if self._articulationInList(el.articulations, 'hammer on') and self._articulationInList(elNext.articulations,
                                                                                                'hammer on'):
            articulation = 'hammer on'
        if self._articulationInList(el.articulations, 'pull off') and self._articulationInList(elNext.articulations,
                                                                                               'pull off'):
            articulation = 'pull off'
        return articulation

    def _articulationInList(self, articulations, name):
        for articulation in articulations:
            if articulation.name == name:
                return True
        return False

    def _isVibrato(self, el):
        for TrillExtension in self.streamObj[music21.expressions.TrillExtension]:
            firstSpannedElement = TrillExtension.getSpannedElements()[0]
            if firstSpannedElement.id == el.id:
                return True
        return False

    def _overlapStartWithThickBarline(self, el, offset, measure):
        if offset == measure.offset and self._measureHasThickBarlineStart(measure):
            return True

    def _overlapEndWithThickBarline(self, el, offset, measure):
        if offset + el.quarterLength == measure.offset + measure.quarterLength and self._measureHasThickBarlineEnd(measure):
            return True

    def _measureHasThickBarlineStart(self, measure):
        for barLine in measure[music21.bar.Barline]:
            if type(barLine) == music21.bar.Repeat and barLine.offset == 0:
                return True

    def _measureHasThickBarlineEnd(self, measure):
        for barLine in measure[music21.bar.Barline]:
            if (type(barLine) == music21.bar.Repeat or barLine.type == 'final') and barLine.offset == measure.quarterLength:
                return True

    def _previous_and_next(self, some_iterable):
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return zip(prevs, items, nexts)

    def _getMeasureByNumber(self, number):
        measures = self.streamObj[music21.stream.Measure]
        for measure in measures:
            if measure.number == number:
                return measure

    def _getSymbol(self, number, accidental):

        if accidental:
            accidentalName = accidental.name
        else:
            accidentalName = "natural"
        symbol = self.alternativeSymbolsDict[str(number)][accidentalName]
        return symbol

    def _getNumberRelativeToChord(self, el, offset, accidentalOriginal):

        chord = self._getCurrentChord(offset)
        chordType = chord.chordKind

        midiNumber = self._getRelativeMidiNumber(chord.root().ps, el.pitch.ps)
        accidental = None

        number = 0

        additions = False

        if midiNumber == 0:
            number = 1

        if midiNumber == 1:
            if additions:
                number = 9
            else:
                number = 2
            accidental = music21.pitch.Accidental('flat')


        if midiNumber == 2:
            if additions and not chordType == 'suspended-second':
                number = 9
            else:
                number = 2

        if midiNumber == 3:
            if 'minor' in chordType or chordType == 'half-diminished' or 'diminished' in chordType:
                number = 3
                accidental = None
            else:
                if additions:
                    number = 9
                else:
                    number = 2
                accidental = music21.pitch.Accidental('sharp')

        if midiNumber == 4:
            number = 3

            if 'minor' in chordType or chordType == 'half-diminished' in chordType or 'diminished' in chordType:
                if additions:
                    number = 11
                    accidental = music21.pitch.Accidental('flat')
                else:
                    number = 4
                    accidental = music21.pitch.Accidental('flat')

        if midiNumber == 5:
            if additions and not 'suspended-fourth' in chordType:
                number = 11
            else:
                number = 4

        if midiNumber == 6:
            if 'half-diminished' in chordType or 'diminished' in chordType:
                number = 5
            else:
                if additions:
                    number = 11
                    accidental = music21.pitch.Accidental('sharp')
                else:
                    number = 4
                    accidental = music21.pitch.Accidental('sharp')

        if midiNumber == 7:
            number = 5
            if 'half-diminished' in chordType or 'diminished' in chordType :
                accidental = music21.pitch.Accidental('sharp')
            if 'augmented' in chordType:
                accidental = music21.pitch.Accidental('flat')


        if midiNumber == 8:
            if 'augmented' in chordType:
                number = 5
            else:
                number = 6
                accidental = music21.pitch.Accidental('flat')

        if midiNumber == 9:
            number = 6
            if chordType == 'diminished-seventh':
                number = 7

        majorSeventhChords = ['major', 'augmented', 'suspended-second', 'suspended-fourth', 'major-sixth']
        minorSeventhChords = ['minor', 'diminished', 'minor-sixth']
        chordsWithoutSeventh = majorSeventhChords + minorSeventhChords

        if midiNumber == 10:
            number = 7
            if chordType in chordsWithoutSeventh:
                if chordType in majorSeventhChords:
                    accidental = music21.pitch.Accidental('flat')
                else:
                    accidental = None
            else:
                accidental = music21.pitch.Accidental('flat')
                if ('minor' in chordType or 'dominant' in chordType or chordType == 'half-diminished') and not 'major' in chordType:
                    accidental = None
                if chordType == 'diminished-seventh':
                    accidental = music21.pitch.Accidental('sharp')

        if midiNumber == 11:
            number = 7
            if chordType in chordsWithoutSeventh:
                if chordType in majorSeventhChords:
                    accidental = None
                else:
                    accidental = music21.pitch.Accidental('sharp')

            if ('minor' in chordType or 'seventh' in chordType or 'ninth' in chordType \
                    or '11th' in chordType or '13th' in chordType or 'half-diminished' in chordType) \
                    and not 'major' in chordType:
                accidental = music21.pitch.Accidental('sharp')
            if chordType == 'diminished-seventh':
                accidental = music21.pitch.Accidental('double-sharp')

        return number, accidental

    def _getCurrentChord(self, offset):
        i = 0
        while i < len(self.chordList) and offset >= self.chordList[i][0]:
            chord = self.chordList[i][1]
            i += 1
        return chord
    def _getRelativeMidiNumber(self, root, pitch):
        return int((pitch - root) % 12)
    def _makeChordList(self):
        chordList = []
        chords = self.streamObj.flatten().getElementsByClass('ChordSymbol')
        for chord in chords:
            offset = chord.getOffsetInHierarchy(self.streamObj)
            chordList.append((offset, chord))
        return chordList

    def _colorwheel(self, circleOfFifthIndex):
        """index must be between 0 and 11"""

        rgbs = [(0.18062, 0.13244, 0.91856, 1.0),
                 (0.44913, 0.17088, 0.97129, 1.0),
                 (0.69537, 0.25408, 0.98496, 1.0),
                 (0.93769, 0.33352, 0.94809, 1.0),
                 (0.98704, 0.57494, 0.75486, 1.0),
                 (0.98761, 0.78074, 0.51946, 1.0),
                 (0.94377, 0.93236, 0.2092, 1.0),
                 (0.7223, 0.87807, 0.079194, 1.0),
                 (0.46484, 0.78619, 0.051424, 1.0),
                 (0.19593, 0.67703, 0.15768, 1.0),
                 (0.27173, 0.52798, 0.46247, 1.0),
                 (0.183, 0.36488, 0.72404, 1.0)]

        return rgbs[circleOfFifthIndex]

