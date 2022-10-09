import json
import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse
from itertools import tee, islice, chain


from sample.plotter.Plotter import Plotter



class PlotterNotes(Plotter):

    def __init__(self, streamObj, Settings, LocationFinder, axs,):

        super().__init__(streamObj, Settings, LocationFinder, axs)


        self.barSpace = Settings.barSpace
        self.noteLowest = Settings.noteLowest

        self.alpha = Settings.alpha
        self.facecolor = Settings.facecolor

        self.key = Settings.key

        self.yShiftNumbers = self._computeYShiftNumbers()
        self.graceNoteCounter = 0

        self.lastLyricEnd = 0
        self.yPosLast = 0

    def plotNotes(self):

        notes = self.streamObj[music21.note.Note]
        chords = self.streamObj[music21.chord.Chord]

        for idx in range(len(notes)):

            el = notes[idx]
            if idx < len(notes) - 1:
                elNext = notes[idx+1]
            else:
                elNext = None

            if type(el) == music21.note.Note:
                self._plotNote(el, elNext)

        for el in chords:
            if type(el) == music21.chord.Chord:
                for note in el.notes:
                    elNext = None
                    self._plotNote(note, elNext, offset=el.getOffsetInHierarchy(self.streamObj))

    def _plotNote(self, el, elNext, offset=None):
        if not offset:
            offset = el.getOffsetInHierarchy(self.streamObj)
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)
        yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.Settings.overlapFactor)
        yPos = yPosLineBase + yPosWithinLine
        offsetLength = el.duration.quarterLength
        xLength = self.LocationFinder._getXLengthFromOffsetLength(offsetLength)
        self._plotRectangle(el, page, xLength, xPos, yPos)
        self._plotNumber(el, elNext, page, xLength, xPos, yPos)

        self._plotArticulation(el, elNext)

        if self.Settings.lyrics:
            self._plotLyric(el, page, xLength, xPos, yPosLineBase)

    def _plotRectangle(self, el, page, xLength, xPos, yPos):
        rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
        xPos += self.Settings.xMarginNote
        xLength -= 2 * self.Settings.xMarginNote
        xLength, xPos = self._extendNotesWhenTied(el, xLength, xPos)
        alpha, facecolor, hatch = self._adjustVisualParametersForGhostNote(el)
        patch = FancyBboxPatch((xPos, yPos),
                               xLength, self.barSpace,
                               boxstyle=f"round, pad=0, rounding_size={self.Settings.radiusCorners}",
                               mutation_aspect=self.Settings.mutationAspect,
                               fc=facecolor, alpha=alpha,
                               edgecolor='black', linewidth=0,
                               hatch=hatch
                               )
        self.axs[page].add_patch(patch)
        self.axs[page].add_patch(rec)
        patch.set_clip_path(rec)

    def _plotNumber(self, el, elNext, page, xLengthBeforeExtension, xPos, yPos):
        if not (el.tie and not (el.tie.type == 'start')):
            number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)


            xShiftNumbers = self._computeXShiftNumbers(el, elNext, xLengthBeforeExtension)

            xPos += xShiftNumbers
            yPos += self.yShiftNumbers

            fontSize = self.Settings.fontSizeNotes
            if not el.duration.linked:
                fontSize = self.Settings.fontSizeGraceNotes

            self.axs[page].text(xPos, yPos, number,
                                fontsize=fontSize,
                                va='baseline', ha='left')

            self._plotAccidental(accidental, fontSize, xPos, yPos, page)

    def _plotLyric(self, el, page, xLength, xPos, yPos):

        lyric = el.lyric
        if el.lyric:
            syllabic = el.lyrics[0].syllabic
            if syllabic == 'begin' or syllabic == 'middle':
                lyric += "-"
        xPosCenter = xPos + self.Settings.xShiftNumberNote / 4

        if xPosCenter < self.lastLyricEnd and self.yPosLast == yPos:
            xPosCenter = self.lastLyricEnd + self.Settings.widthNumberNote * 0.3

        self.yPosLast = yPos
        yPos -= self.Settings.barSpace * 0.5

        self.renderer = self.axs[page].figure.canvas.get_renderer()

        plottedLyric = self.axs[page].text(xPosCenter, yPos, lyric,
                            fontsize=5,
                            va='baseline', ha='left')
        lyricStart = xPosCenter

        bb = plottedLyric.get_window_extent(renderer=self.renderer).transformed(self.axs[page].transData.inverted())
        lyricWidth = bb.width

        self.lastLyricEnd = lyricStart + lyricWidth
        if lyric:
            if lyric[-1] == "-":
                self.lastLyricEnd -= 0.3 * self.Settings.widthNumberNote

    def _adjustVisualParametersForGhostNote(self, el):
        facecolor = self.facecolor
        alpha = self.alpha
        hatch = None
        # ghost note
        if el.notehead == 'x':
            facecolor = 'grey'
            alpha = 0.15
            hatch = 'xxxxx'  # this controls the fine graindedness of the x pattern? TODO: make notebook
        return alpha, facecolor, hatch

    def _extendNotesWhenTied(self, el, xLength, xPos):
        xExtensionNoteWhenTied = self.Settings.radiusCorners + self.Settings.xMarginNote
        if el.tie:
            if el.tie.type == 'start':
                xLength += xExtensionNoteWhenTied
            elif el.tie.type == 'continue':
                xLength += 2 * xExtensionNoteWhenTied
                xPos -= xExtensionNoteWhenTied
            elif el.tie.type == 'stop':
                xLength += xExtensionNoteWhenTied
                xPos -= xExtensionNoteWhenTied
        return xLength, xPos

    def _computeXShiftNumbers(self, el, elNext, xLengthBeforeExtension):

        if el.duration.linked:  # not grace note

            xShiftNumbers = self.Settings.xShiftNumberNote
            if xLengthBeforeExtension < (2 * self.Settings.xShiftNumberNote + self.Settings.widthNumberNote) and (
            not el.tie):
                xShiftNumbers = 0.5 * xLengthBeforeExtension - 0.5 * self.Settings.widthNumberNote

        # grace notes
        elif el.beams.beamsList:  # multiple grace notes
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

        else:      # one grace note
            xShiftNumbers = 0


        return xShiftNumbers


    def _computeYShiftNumbers(self):

        yShiftNumbers = (self.barSpace - self.Settings.capsizeNumberNote) / 2

        return yShiftNumbers


    def _plotArticulation(self, el, elNext):
        if elNext:
            articulation = self._getArticulation(el, elNext)
            if articulation:
                offset = el.getOffsetInHierarchy(self.streamObj)
                page, yPosLineBase, xPosStart = self.LocationFinder.getLocation(offset)

                yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.Settings.overlapFactor)
                yPos1 = yPosLineBase + yPosWithinLine
                yPosWithinLine = (elNext.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.Settings.overlapFactor)
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
                self.axs[page].text(xPos, yPosBaseline, "H", ha='center', va='baseline', font='Arial', fontsize=7, fontstyle='normal', zorder=2)



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

    def _previous_and_next(self, some_iterable):
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return zip(prevs, items, nexts)
