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
        self.overlapFactor = settings["overlapFactor"]
        self.noteLowest = noteLowest

        self.alpha = settings["alpha"]
        self.facecolor = settings["facecolor"]

        self.yShiftNumbers = settings['yShiftNumbers']
        self.xShiftNumbersFixed = settings['xShiftNumbersPerWidthFixed']
        self.xWidthNumber = settings["widthNumber"]

        self.xExtensionNoteWhenTied = settings["radiusCorners"] + settings["xPadding"]

        self.key = key

    def plotNotes(self):

        # loop through elements in stream
        for el in self.streamObj.recurse():

            if type(el) == music21.note.Note:

                offset = el.getOffsetInHierarchy(self.streamObj)  # + self.xExtensionNoteWhenTied
                line, offsetLine = self.LocationFinder.getLocation(offset)

                yPosLineBase = self.CanvasCreator.getYPosLineBase(line)

                yPosWithinLine = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.overlapFactor)

                yPos = yPosLineBase + yPosWithinLine

                page = self.linesToPage[line]

                offsetLength = el.duration.quarterLength  # - 2 * self.xExtensionNoteWhenTied
                facecolor = self.facecolor
                linewidth = 0
                alpha = self.alpha
                hatch = None


                xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)
                xLength = self.CanvasCreator.getXLengthFromOffsetLength(offsetLength)


                rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
                xLengthBeforeExtension = xLength

                xPos += self.settings["xPadding"]
                xLength -= 2 * self.settings["xPadding"]

                if el.tie:
                    if el.tie.type == 'start':
                        xLength += self.xExtensionNoteWhenTied
                    elif el.tie.type == 'continue':
                        xLength += 2 * self.xExtensionNoteWhenTied
                        xPos -= self.xExtensionNoteWhenTied
                    elif el.tie.type == 'stop':
                        xLength += self.xExtensionNoteWhenTied
                        xPos -= self.xExtensionNoteWhenTied

                # ghost note
                ghostNote = False
                if el.notehead == 'x':
                    ghostNote = True
                    facecolor = 'grey'
                    linewidth = 0
                    alpha = 0.15
                    hatch = 'xxxxx'   # this controls the fine graindedness of the x pattern? TODO: make notebook


                

                patch = FancyBboxPatch((xPos, yPos),
                                       xLength, self.barSpace,
                                       boxstyle=f"round, pad=0, rounding_size={self.settings['radiusCorners']}",
                                       mutation_aspect=self.settings["mutationAspect"],
                                       fc=facecolor, alpha=alpha,
                                       edgecolor='black', linewidth=linewidth,
                                       hatch=hatch
                                       )

                self.axs[page].add_patch(patch)
                self.axs[page].add_patch(rec)
                patch.set_clip_path(rec)


                # plot numbers
                if not (el.tie and not (el.tie.type == 'start')):
                    number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)
                    if accidental:
                        if accidental.name == 'sharp':
                            number = f"$ {{}}^\\# {number}$"
                        elif accidental.name == 'flat':
                            number = f"$ {{}}^b {number}$"
                    else:
                        number = f"${number}$"

                    xCenterNumbers = 0.015625
                    xShiftNumbers = xCenterNumbers + 0.5 * self.xWidthNumber
                    if xLengthBeforeExtension < (2 * xCenterNumbers):
                        xShiftNumbers = 0.5 * xLengthBeforeExtension + 0.5 * self.xWidthNumber

                    self.axs[page].text(xPos + xShiftNumbers,
                                          yPos + self.yShiftNumbers + 0.5 * self.barSpace,
                                          number, fontsize=self.settings['fontSizeNotes'],
                                          va='center', ha='right')


