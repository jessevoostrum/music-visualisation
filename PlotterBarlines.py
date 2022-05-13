import music21
from matplotlib.patches import Circle
import numpy as np


class PlotterBarlines:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        self.axs = CanvasCreator.getAxs()


    def plotBarlines(self):

        for measure in self.streamObj.recurse().getElementsByClass(music21.stream.Measure):

            self.plotMeasureBarlines(measure)

            if self.settings["subdivision"] >= 1:
                self.plotSubdivisionBarlines(measure, 1)

            if self.settings["subdivision"] >= 2:
                self.plotSubdivisionBarlines(measure, 2)

            self._plotRepeatBracket(measure)

    def plotMeasureBarlines(self, measure):
        if not measure.number == 0:
            self.plotVBar(measure.offset, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], True)

        offsetEndMeasure = measure.offset + measure.quarterLength
        self.plotVBar(offsetEndMeasure, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], False)

        for barLine in measure[music21.bar.Barline]:
            if type(barLine) == music21.bar.Repeat:
                if barLine.direction == 'start':
                    start = True
                else:
                    start = False
                offset = measure.offset + barLine.offset

                self.plotVBar(offset, self.settings["lineWidth0"] , self.settings["heightBarline0Extension"], start)

    def plotSubdivisionBarlines(self, measure, subdivision):
        if subdivision == 1:
            step = 1
            lineWidth = self.settings["lineWidth1"]
        elif subdivision == 2:
            step = 0.25
            lineWidth = self.settings["lineWidth2"]

        for t in np.arange(0, measure.quarterLength, step=step):
            if measure.number == 0:
                offset = measure.offset + measure.quarterLength - t
            elif measure.number >= 1:
                offset = measure.offset + t

            self.plotVBar(offset, lineWidth, 0, True)

    def plotVBar(self, offset, lineWidth, extension, start):

        line, offsetLine = self.LocationFinder.getLocation(offset, start=start)
        page = self.CanvasCreator.getLinesToPage()[line]

        yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"]

        xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)

        self.axs[page].vlines(xPos, yPosLow, yPosHigh + extension,
                              linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)

    def _plotDots(self, offset, start):
        line, offsetLine = self.LocationFinder.getLocation(offset, start=start)
        page = self.CanvasCreator.getLinesToPage()[line]

        yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"]
        yPos = (yPosHigh + yPosLow)/2

        xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)

        shift = - 0.003
        if start:
            shift = shift * -1

        xPos = xPos + shift

        patch = Circle(xPos, yPos)

        self.axs[page].add_patch(patch)

    def _plotRepeatBracket(self, measure):
        if measure.getSpannerSites():
            spanner = measure.getSpannerSites()[0]
            if type(spanner) == music21.spanner.RepeatBracket:

                offset = measure.offset

                line, offsetLine = self.LocationFinder.getLocation(offset, start=True)
                page = self.CanvasCreator.getLinesToPage()[line]

                yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
                yPosHigh = yPosLineBase + self.settings["yMax"]

                xPosStart = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)
                xPosEnd = self.CanvasCreator.getXPosFromOffsetLine(offsetLine + measure.quarterLength)

                lineWidth = self.settings["lineWidth0"]
                self.axs[page].hlines(yPosHigh + 0.02, xPosStart, xPosEnd,
                                      linestyle='dotted', linewidth=lineWidth, color='grey', zorder=.5)

                if spanner.isFirst(measure):
                    number = spanner.number + "."
                    self.axs[page].text(xPosStart + 0.0055, yPosHigh + 0.01,  number)

                    self.axs[page].vlines(xPosStart, yPosHigh + 0.01, yPosHigh + 0.02,
                                          linestyle='dotted', linewidth=lineWidth, color='grey', zorder=.5)

                if spanner.isLast(measure):
                    # self.axs[page].vlines(xPosEnd, yPosHigh + 0.01, yPosHigh + 0.02,
                    #                       linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)

                    pass

