import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle


class PlotterNotes:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator,  noteLowest, key):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder

        self.axs1D = CanvasCreator.getAxs1D()
        self.widthAxs = CanvasCreator.getWidthAx()

        self.barSpace = settings["barSpace"]
        self.overlapFactor = settings["overlapFactor"]
        self.noteLowest = noteLowest

        self.alpha = settings["alpha"]
        self.facecolor = settings["facecolor"]

        self.yShiftNumbers = settings['yShiftNumbers']
        self.xShiftNumbersFixed = settings['xShiftNumbersPerWidthFixed'] * self.widthAxs
        self.xWidthNumber = settings["widthNumber"] * self.widthAxs

        self.xExtensionNoteWhenTied = settings["xExtensionNoteWhenTiedRelative"] * self.widthAxs

        self.key = key

    def plotNotes(self):

        # loop through elements in stream
        for el in self.streamObj.recurse():

            if type(el) == music21.note.Note:

                yPos = (el.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.overlapFactor)
                offset = el.getOffsetInHierarchy(self.streamObj)  # + self.xExtensionNoteWhenTied
                line, xPos = self.LocationFinder.getLocation(offset)
                xLength = el.duration.quarterLength  # - 2 * self.xExtensionNoteWhenTied
                facecolor = self.facecolor
                linewidth = 0
                alpha = self.alpha
                hatch = None

                # tied notes
                # if el.tie:
                #     if el.tie.type == 'start':
                #         xLength += self.xExtensionNoteWhenTied
                #     elif el.tie.type == 'continue':
                #         xLength += 2 * self.xExtensionNoteWhenTied
                #         xPos -= self.xExtensionNoteWhenTied
                #     elif el.tie.type == 'stop':
                #         xLength += self.xExtensionNoteWhenTied
                #         xPos -= self.xExtensionNoteWhenTied

                rec = Rectangle((xPos, yPos), xLength, self.barSpace, facecolor="none", edgecolor="none")
                xLengthBeforeExtension = xLength

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


                # glissando
                if el.getSpannerSites():
                    sp = el.getSpannerSites()[0]
                    if type(sp) == music21.spanner.Glissando:
                        endGlissando = False
                        if sp.isFirst(el):
                            xLength += self.xExtensionNoteWhenTied
                            noteTarget = sp.getLast()
                            # offsetTarget = noteTarget.getOffsetInHierarchy(self.streamObj)
                            yTarget = (noteTarget.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.overlapFactor)
                            yMiddle = (yTarget + yPos) / 2
                            patch = Polygon([[xPos, yPos], [xPos, yPos + self.barSpace],
                                             [xPos + xLength, yMiddle + self.barSpace], [xPos + xLength, yMiddle]],
                                            facecolor=self.facecolor,
                                            alpha=self.alpha)
                            self.axs1D[line].add_patch(patch)

                        elif sp.isLast(el):
                            endGlissando = True
                            xLength += self.xExtensionNoteWhenTied
                            xPos -= self.xExtensionNoteWhenTied

                            noteOrigin = sp.getFirst()
                            yOrigin = (noteOrigin.pitch.ps - self.noteLowest) * self.barSpace * (1 - self.overlapFactor)
                            yMiddle = (yOrigin + yPos) / 2

                            patch = Polygon([[xPos, yMiddle], [xPos, yMiddle + self.barSpace],
                                             [xPos + xLength, yPos + self.barSpace], [xPos + xLength, yPos]],
                                            facecolor=self.facecolor,
                                            alpha=self.alpha)
                            self.axs1D[line].add_patch(patch)

                        if not (el.tie and not (el.tie.type == 'start')):
                            number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(el.pitch)
                            if accidental:
                                if accidental.name == 'sharp':
                                    number = f"$ {{}}^\\# {number}$"
                                elif accidental.name == 'flat':
                                    number = f"$ {{}}^b {number}$"

                            if endGlissando:
                                xPos += xLength - 4 * self.xShiftNumbers
                            self.axs1D[line].text(xPos + self.xShiftNumbers,
                                                  yPos + self.yShiftNumbers + 0.5 * self.barSpace,
                                                  number,
                                                  va='center')

                        continue

                patch = FancyBboxPatch((xPos, yPos),
                                       xLength, self.barSpace,
                                       boxstyle="round, pad=-0.01, rounding_size=0.1",
                                       mutation_aspect=0.02,
                                       fc=facecolor, alpha=alpha,
                                       edgecolor='black', linewidth=linewidth,
                                       hatch=hatch
                                       )

                self.axs1D[line].add_patch(patch)
                self.axs1D[line].add_patch(rec)
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

                    xCenterNumbers = 0.015625 * self.settings['xMax']
                    xShiftNumbers = xCenterNumbers + 0.5 * self.xWidthNumber
                    if xLengthBeforeExtension < (2 * xCenterNumbers):
                        xShiftNumbers = 0.5 * xLengthBeforeExtension + 0.5 * self.xWidthNumber

                    self.axs1D[line].text(xPos + xShiftNumbers,
                                          yPos + self.yShiftNumbers + 0.5 * self.barSpace,
                                          number, fontsize=self.settings['fontSizeNotes'],
                                          va='center', ha='right')


