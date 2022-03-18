import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


class PlotterBarlines:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator, yMin, yMax,):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        self.axs = CanvasCreator.getAxs()
        self.widthAxs = CanvasCreator.getWidthAx()

        self.yMin = yMin
        self.yMax = yMax

        self.subdivision = settings["subdivision"]


    def plotBarlines(self):
        heightBarline0Extension = self.settings["heightBarline0Extension"]
        assert (heightBarline0Extension < self.settings["vMarginLineTop"]), "barlineExtension should be smaller than vMarginLineTop"
        linewidth_0 = self.settings["linewidth_0"]
        linewidth_1 = self.settings["linewidth_1"]
        linewidth_2 = self.settings["linewidth_2"]

        for measure in self.streamObj.recurse().getElementsByClass(music21.stream.Measure):
            line = self.LocationFinder.getLocation(measure.offset)[0]  #this is assuming the whole measure stays on the same line
            page = self.CanvasCreator.getLinesToPage()[line]
            yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
            yPosLow = yPosLineBase + self.yMin
            yPosHigh = yPosLineBase + self.yMax
            if not measure.number == 0:
                # vline start measure
                line, xPos = self.LocationFinder.getLocation(measure.offset)
                self.axs[page].vlines(xPos, yPosLow, yPosHigh + heightBarline0Extension,
                                        linestyle='solid', linewidth=linewidth_0, color='grey', zorder=.5)
            # vline end measure
            offsetEndMeasure = measure.offset + measure.quarterLength
            line, xPos = self.LocationFinder.getLocation(offsetEndMeasure, start=False)
            self.axs[page].vlines(xPos, yPosLow, yPosHigh + heightBarline0Extension,
                                    linestyle='solid', linewidth=linewidth_0, color='grey', zorder=.5)

            if not measure.number == 0:
                if self.subdivision >= 1:
                    for t in np.arange(0, measure.quarterLength, step=1):
                        offset = measure.offset + t
                        line, xPos = self.LocationFinder.getLocation(offset, start=True)
                        self.axs[page].vlines(xPos, yPosLow, yPosHigh,
                                linestyle='solid', linewidth=linewidth_1, color='grey', zorder=.5)

                if self.subdivision >= 2:
                    for t in np.arange(0, measure.quarterLength, step=.25):
                        offset = measure.offset + t
                        line, xPos = self.LocationFinder.getLocation(offset, start=True)
                        self.axs[page].vlines(xPos, yPosLow, yPosHigh,
                                                linestyle='solid', linewidth=linewidth_2, color='grey', zorder=.5)

            if measure.number == 0:
                 if self.subdivision >= 1:
                     for t in np.arange(0, measure.quarterLength, step=1):
                         offset = measure.offset + measure.quarterLength - t
                         line, xPos = self.LocationFinder.getLocation(offset, start=True)
                         self.axs[page].vlines(xPos, yPosLow, yPosHigh,
                                                 linestyle='solid', linewidth=linewidth_1, color='grey', zorder=.5)

                 if self.subdivision >= 2:
                     for t in np.arange(0, measure.quarterLength, step=.25):
                         offset = measure.offset + measure.quarterLength - t
                         line, xPos = self.LocationFinder.getLocation(offset, start=True)
                         self.axs[page].vlines(xPos, yPosLow, yPosHigh,
                                                 linestyle='solid', linewidth=linewidth_2, color='grey', zorder=.5)

