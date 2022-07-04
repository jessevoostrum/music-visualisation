import json
import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle

from Plotter import Plotter



class PlotterNotes(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator,  noteLowest, key):

        super().__init__(CanvasCreator.getAxs())

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        # self.axs = CanvasCreator.getAxs()
        self.linesToLineOnPage = CanvasCreator.getLinesToLineOnPage()
        self.linesToPage = CanvasCreator.getLinesToPage()

        self.barSpace = settings["barSpace"]
        self.noteLowest = noteLowest

        self.alpha = settings["alpha"]
        self.facecolor = settings["facecolor"]

        self.key = key

        self.yShiftNumbers = self.computeYShiftNumbers()

    def plotNotes(self):

        # loop through elements in stream
        for el in self.streamObj.recurse():

            if type(el) == music21.note.Note:

                self._plotNote(el)

            elif type(el) == music21.chord.Chord:

                for note in el.notes:
                    self._plotNote(note, offset=el.getOffsetInHierarchy(self.streamObj))

    def _plotNote(self, el, offset=None):
        if not offset:
            offset = el.getOffsetInHierarchy(self.streamObj)  # + self.xExtensionNoteWhenTied
        line, offsetLine = self.LocationFinder.getLocation(offset)
        yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
        yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.settings["overlapFactor"])
        yPos = yPosLineBase + yPosWithinLine
        page = self.linesToPage[line]
        offsetLength = el.duration.quarterLength  # - 2 * self.xExtensionNoteWhenTied
        xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)
        xLength = self.CanvasCreator.getXLengthFromOffsetLength(offsetLength)
        self.plotRectangle(el, page, xLength, xPos, yPos)
        self.plotNumber(el, page, xLength, xPos, yPos)

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

    def plotNumber(self, el, page, xLengthBeforeExtension, xPos, yPos):
        if not (el.tie and not (el.tie.type == 'start')):
            number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)


            xShiftNumbers = self.settings["xShiftNumberNote"]
            if xLengthBeforeExtension < (2 * self.settings["xShiftNumberNote"] + self.settings["widthNumberNote"]) and (not el.tie):
                xShiftNumbers = 0.5 * xLengthBeforeExtension - 0.5 * self.settings["widthNumberNote"]

            xPos += xShiftNumbers
            yPos += self.yShiftNumbers

            self.axs[page].text(xPos, yPos, number,
                                fontsize=self.settings['fontSizeNotes'],
                                va='baseline', ha='left')

            self.plotAccidental(accidental, self.settings['fontSizeNotes'], xPos, yPos, page)

    def plotLyric(self, el, page, xLength, xPos, yPos):
        lyric = el.lyric
        if el.lyric:
            syllabic = el.lyrics[0].syllabic
            if syllabic == 'begin' or syllabic == 'middle':
                lyric += "-"
        xPosCenter = xPos # + 0.5 * xLength
        yPos -= self.settings['barSpace'] * 0.5
        self.axs[page].text(xPosCenter, yPos, lyric,
                            fontsize=7,
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


    def computeYShiftNumbers(self):

        yShiftNumbers = (self.barSpace - self.settings['capsizeNumberNote']) / 2

        return yShiftNumbers

