import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


class PlotterBarlines:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        self.axs = CanvasCreator.getAxs()
        self.widthAxs = CanvasCreator.getWidthAx()


    def plotBarlines(self):

        for measure in self.streamObj.recurse().getElementsByClass(music21.stream.Measure):

            self.plotMeasureBarlines(measure)

            if self.settings["subdivision"] >= 1:
                self.plotSubdivisionBarlines(measure, 1)

            if self.settings["subdivision"] >= 2:
                self.plotSubdivisionBarlines(measure, 2)

    def plotMeasureBarlines(self, measure):
        if not measure.number == 0:
            self.plotVBar(measure.offset, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], True)

        offsetEndMeasure = measure.offset + measure.quarterLength
        self.plotVBar(offsetEndMeasure, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], False)

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