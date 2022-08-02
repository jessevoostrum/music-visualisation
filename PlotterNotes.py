import json
import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
from itertools import tee, islice, chain


from Plotter import Plotter



class PlotterNotes(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator,):

        super().__init__(CanvasCreator.getAxs())

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        # self.axs = CanvasCreator.getAxs()
        self.linesToLineOnPage = CanvasCreator.getLinesToLineOnPage()
        self.linesToPage = CanvasCreator.getLinesToPage()

        self.barSpace = settings["barSpace"]
        self.noteLowest = settings["noteLowest"]

        self.alpha = settings["alpha"]
        self.facecolor = settings["facecolor"]

        self.key = settings["key"]

        self.yShiftNumbers = self.computeYShiftNumbers()
        self.graceNoteCounter = 0

    def plotNotes(self):

        for elPrev, el, elNext in self.previous_and_next(self.streamObj.recurse()):

            if type(el) == music21.note.Note:

                self._plotNote(el, elNext)

            elif type(el) == music21.chord.Chord:

                for note in el.notes:
                    self._plotNote(note, elNext, offset=el.getOffsetInHierarchy(self.streamObj))

    def _plotNote(self, el, elNext, offset=None):
        if not offset:
            offset = el.getOffsetInHierarchy(self.streamObj)
        page, yPosLineBase, xPos = self.CanvasCreator.getLocation(offset)
        yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.settings["overlapFactor"])
        yPos = yPosLineBase + yPosWithinLine
        offsetLength = el.duration.quarterLength
        xLength = self.CanvasCreator.getXLengthFromOffsetLength(offsetLength)
        self.plotRectangle(el, page, xLength, xPos, yPos)
        self.plotNumber(el, elNext, page, xLength, xPos, yPos)

        if self.settings["lyrics"]:
            self.plotLyric(el, page, xLength, xPos, yPosLineBase)

    def plotRectangle(self, el, page, xLength, xPos, yPos):
        rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
        xPos += self.settings["xMarginNote"]
        xLength -= 2 * self.settings["xMarginNote"]
        xLength, xPos = self.extendNotesWhenTied(el, xLength, xPos)
        alpha, facecolor, hatch = self.adjustVisualParametersForGhostNote(el)
        patch = FancyBboxPatch((xPos, yPos),
                               xLength, self.barSpace,
                               boxstyle=f"round, pad=0, rounding_size={self.settings['radiusCorners']}",
                               mutation_aspect=self.settings["mutationAspect"],
                               fc=facecolor, alpha=alpha,
                               edgecolor='black', linewidth=0,
                               hatch=hatch
                               )
        self.axs[page].add_patch(patch)
        self.axs[page].add_patch(rec)
        patch.set_clip_path(rec)

    def plotNumber(self, el, elNext, page, xLengthBeforeExtension, xPos, yPos):
        if not (el.tie and not (el.tie.type == 'start')):
            number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)


            xShiftNumbers = self._computeXShiftNumbers(el, elNext, xLengthBeforeExtension)

            xPos += xShiftNumbers
            yPos += self.yShiftNumbers

            fontSize = self.settings['fontSizeNotes']
            if not el.duration.linked:
                fontSize = self.settings['fontSizeGraceNotes']

            self.axs[page].text(xPos, yPos, number,
                                fontsize=fontSize,
                                va='baseline', ha='left')

            self.plotAccidental(accidental, fontSize, xPos, yPos, page)

    def plotLyric(self, el, page, xLength, xPos, yPos):
        lyric = el.lyric
        if el.lyric:
            syllabic = el.lyrics[0].syllabic
            if syllabic == 'begin' or syllabic == 'middle':
                lyric += "-"
        xPosCenter = xPos + self.settings["xShiftNumberNote"] / 2
        yPos -= self.settings['barSpace'] * 0.5
        self.axs[page].text(xPosCenter, yPos, lyric,
                            fontsize=5,
                            va='baseline', ha='left')

    def adjustVisualParametersForGhostNote(self, el):
        facecolor = self.facecolor
        alpha = self.alpha
        hatch = None
        # ghost note
        if el.notehead == 'x':
            facecolor = 'grey'
            alpha = 0.15
            hatch = 'xxxxx'  # this controls the fine graindedness of the x pattern? TODO: make notebook
        return alpha, facecolor, hatch

    def extendNotesWhenTied(self, el, xLength, xPos):
        xExtensionNoteWhenTied = self.settings["radiusCorners"] + self.settings["xMarginNote"]
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

            xShiftNumbers = self.settings["xShiftNumberNote"]
            if xLengthBeforeExtension < (2 * self.settings["xShiftNumberNote"] + self.settings["widthNumberNote"]) and (
            not el.tie):
                xShiftNumbers = 0.5 * xLengthBeforeExtension - 0.5 * self.settings["widthNumberNote"]

        # grace notes
        elif el.beams.beamsList:  # multiple grace notes
            if el.beams.getTypes()[0] == 'start':  #
                xShiftNumbers = 0
                self.graceNoteCounter += 1
            elif el.beams.getTypes()[0] == 'continue':
                if elNext.beams.getTypes()[0] == 'continue': # max of 4 grace notes supported
                    xShiftNumbers = self.settings["xShiftNumberNote"] / 4
                    self.graceNoteCounter += 1
                elif elNext.beams.getTypes()[0] == 'stop':
                    xShiftNumbers = self.settings["xShiftNumberNote"] * self.graceNoteCounter / (self.graceNoteCounter + 2)
                    self.graceNoteCounter += 1
            elif el.beams.getTypes()[0] == 'stop':
                xShiftNumbers = self.settings["xShiftNumberNote"] * self.graceNoteCounter / (self.graceNoteCounter + 1)
                self.graceNoteCounter = 0

        else:      # one grace note
            xShiftNumbers = 0


        return xShiftNumbers


    def computeYShiftNumbers(self):

        yShiftNumbers = (self.barSpace - self.settings['capsizeNumberNote']) / 2

        return yShiftNumbers

    def previous_and_next(self, some_iterable):
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return zip(prevs, items, nexts)
