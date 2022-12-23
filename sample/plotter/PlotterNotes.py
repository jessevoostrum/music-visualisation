import json
import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse
from matplotlib import cm
from itertools import tee, islice, chain
import colorcet as cc



from sample.plotter.Plotter import Plotter



class PlotterNotes(Plotter):

    def __init__(self, streamObj, Settings, LocationFinder, axs,):

        super().__init__(streamObj, Settings, LocationFinder, axs)

        self.barSpace = Settings.barSpace
        self.noteLowest = Settings.noteLowest

        self.key = Settings.key

        self.yShiftNumbers = self._computeYShiftNumbers()
        self.graceNoteCounter = 0

        self.lastLyricEnd = 0
        self.yPosLineBaseLast = 0

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
        if offset is None:
            offset = el.getOffsetInHierarchy(self.streamObj)
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)
        yPosWithinLine = self._yPosWithinLine(el)
        yPos = yPosLineBase + yPosWithinLine
        offsetLength = el.duration.quarterLength
        xLength = self.LocationFinder._getXLengthFromOffsetLength(offsetLength)

        slope = None
        if self._isGlissando(el):
            slope = self._plotParallelogram(page, el, elNext, xPos, xLength,  yPos, yPosLineBase)

        else:
            self._plotRectangle(page, el, elNext, xPos, xLength,  yPos)

        self._plotNumber(page, el, elNext, xPos, xLength, yPos, slope)

        self._plotArticulation(el, elNext)

        if self.Settings.lyrics:
            self._plotLyric(page, el, xPos, yPosLineBase)

    def _yPosWithinLine(self, el):
        yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.Settings.overlapFactor)
        return yPosWithinLine

    def _plotRectangle(self, page, el, elNext, xPos, xLength,  yPos):
        if self._isGlissando(el):
            return

        rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
        xPos += self.Settings.xMarginNote
        xLength -= 2 * self.Settings.xMarginNote
        xLength, xPos = self._extendNotesWhenTied(el, xLength, xPos)

        alpha, facecolor, hatch = self._adjustVisualParameters(el)
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

    def _plotParallelogram(self, page, el, elNext, xPos, xLength,  yPos, yPosLineBase):
        # see https://stackoverflow.com/questions/19270673/matplotlib-radius-in-polygon-edges-is-it-possible for
        # rounded corners

        sp = el.getSpannerSites()[0]
        alpha, facecolor, hatch = self._adjustVisualParameters(el)

        if self._isStartGlissando(el):
            noteTarget = sp.getLast()

            yTarget = self._yPosWithinLine(noteTarget) + yPosLineBase
            yMiddle = (yTarget + yPos) / 2

            leftBottom = [xPos, yPos]
            leftTop = [xPos, yPos + self.barSpace]
            rightBottom = [xPos + xLength, yMiddle + self.barSpace]
            rightTop = [xPos + xLength, yMiddle]

        else:
            noteOrigin = sp.getFirst()
            yOrigin = self._yPosWithinLine(noteOrigin) + yPosLineBase

            yMiddle = (yOrigin + yPos) / 2

            leftBottom = [xPos, yMiddle]
            leftTop = [xPos, yMiddle + self.barSpace]
            rightBottom = [xPos + xLength, yPos + self.barSpace]
            rightTop = [xPos + xLength, yPos]

        patch = Polygon([leftBottom, leftTop, rightBottom, rightTop], facecolor=facecolor, alpha=alpha)
        self.axs[page].add_patch(patch)

        slope = (rightBottom[1] - leftBottom[1]) / xLength
        return slope

    def _plotNumber(self, page, el, elNext, xPos, xLengthBeforeExtension, yPos, slope):
        if not (el.tie and not (el.tie.type == 'start')):
            number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)

            xShiftNumbers = self._computeXShiftNumbers(el, elNext, xLengthBeforeExtension)

            slopeFactor = .4
            horizontalAlignment = 'left'
            if self._isStartGlissando(el):
                yPos += slope * self.barSpace * slopeFactor
                pass
            elif self._isEndGlissando(el):
                xPos += xLengthBeforeExtension
                yPos -= slope * self.barSpace * slopeFactor
                horizontalAlignment = 'right'
            else:
                xPos += xShiftNumbers

            yPos += self.yShiftNumbers

            fontSize = self.Settings.fontSizeNotes
            if not el.duration.linked:
                fontSize = self.Settings.fontSizeGraceNotes

            self.axs[page].text(xPos, yPos, number,
                                fontsize=fontSize,
                                va='baseline', ha=horizontalAlignment)

            self._plotAccidental(accidental, fontSize, xPos, yPos, page)

    def _plotLyric(self, page, el, xPos, yPosLineBase):

        lyric = el.lyric
        if el.lyric:
            syllabic = el.lyrics[0].syllabic
            if syllabic == 'begin' or syllabic == 'middle':
                lyric += "-"
        xPosCenter = xPos + self.Settings.xShiftNumberNote / 4

        if xPosCenter < self.lastLyricEnd and self.yPosLineBaseLast == yPosLineBase:
            xPosCenter = self.lastLyricEnd + self.Settings.widthNumberNote * 0.3

        self.yPosLineBaseLast = yPosLineBase

        yPos = yPosLineBase

        self.renderer = self.axs[page].figure.canvas.get_renderer()

        plottedLyric = self.axs[page].text(xPosCenter, yPos, lyric,
                            fontsize=self.Settings.fontSizeLyrics,
                            va='top', ha='left')
        lyricStart = xPosCenter

        bb = plottedLyric.get_window_extent(renderer=self.renderer).transformed(self.axs[page].transData.inverted())
        lyricWidth = bb.width

        self.lastLyricEnd = lyricStart + lyricWidth
        if lyric:
            if lyric[-1] == "-":
                self.lastLyricEnd -= 0.3 * self.Settings.widthNumberNote
        

    def _adjustVisualParameters(self, el):

        facecolor = self.Settings.facecolor
        alpha = self.Settings.alpha
        hatch = None


        if self.Settings.coloursCircleOfFifths:

            pitchKey = self.key.getTonic().ps
            pitchNote = el.pitch.ps
            relativePitch = (pitchNote - pitchKey) % 12
            colormapIndex = self._relativePitchToCircleOfFifthsIndex(relativePitch) / 12

            # facecolor = cm.get_cmap('cet_fire')(colormapIndex)
            facecolor = cc.cm.colorwheel(colormapIndex)
            alpha = .5

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
        return alpha, facecolor, hatch

    def _relativePitchToCircleOfFifthsIndex(self, relativePitch):
        pitchesCircleOfFifths = [(i*7) % 12 for i in range(12)]
        return pitchesCircleOfFifths.index(relativePitch)

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
        elif self._isEndGlissando(el):
            if self._isStartGlissando(el):
                xLength += xExtensionNoteWhenTied
            elif self._isEndGlissando(el):
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


