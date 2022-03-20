import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle


class PlotterNotes:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator,  noteLowest, key):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        self.axs = CanvasCreator.getAxs()
        self.widthAxs = CanvasCreator.getWidthAx()
        self.linesToLineOnPage = CanvasCreator.getLinesToLineOnPage()
        self.linesToPage = CanvasCreator.getLinesToPage()

        self.barSpace = settings["barSpace"]
        self.noteLowest = noteLowest

        self.alpha = settings["alpha"]
        self.facecolor = settings["facecolor"]

        self.key = key

    def plotNotes(self):

        # loop through elements in stream
        for el in self.streamObj.recurse():

            if type(el) == music21.note.Note:

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

    def plotRectangle(self, el, page, xLength, xPos, yPos):
        xPos += self.settings["xMarginNote"]
        xLength -= 2 * self.settings["xMarginNote"]
        rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
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
            if accidental:
                if accidental.name == 'sharp':
                    number = f"$ {{}}^\\# {number}$"
                elif accidental.name == 'flat':
                    number = f"$ {{}}^b {number}$"
            else:
                number = f"${number}$"

            xShiftNumbers = self.settings["xShiftCenterOfNumber"] + 0.5 * self.settings["xWidthNumber"]
            if xLengthBeforeExtension < (2 * self.settings["xShiftCenterOfNumber"]):
                xShiftNumbers = 0.5 * xLengthBeforeExtension + 0.5 * self.settings["xWidthNumber"]

            self.axs[page].text(xPos + xShiftNumbers,
                                yPos + self.settings["yShiftNumbers"] + 0.5 * self.barSpace,
                                number, fontsize=self.settings['fontSizeNotes'],
                                va='center', ha='right')


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




