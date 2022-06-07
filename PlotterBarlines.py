import inspect
import music21
from matplotlib.patches import Ellipse, Rectangle
import matplotlib.font_manager as fm
import numpy as np


fp1=fm.FontProperties(fname="/Users/jvo/Downloads/freefont-20120503/FreeSerif.ttf")
fp1=fm.FontProperties(fname="/Users/jvo/Downloads/symbola/Symbola.ttf")

fp2=fm.FontProperties(fname="/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/OH no Type Company Order #e6cd109/Vulf Mono/Desktop/VulfMono-LightItalic.otf")

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

            self._plotRepeatBrackets(measure)
            self._plotRepeatExpressions(measure)

    def plotMeasureBarlines(self, measure):
        if not measure.number == 0:
            self.plotVBar(measure.offset, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], start=True)

        offsetEndMeasure = measure.offset + measure.quarterLength
        self.plotVBar(offsetEndMeasure, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], start=False)

        for barLine in measure[music21.bar.Barline]:
            offset = measure.offset + barLine.offset

            if type(barLine) == music21.bar.Repeat:

                if barLine.direction == 'start':
                    start = True
                else:
                    start = False

                self.plotVBar(offset, self.settings["lineWidth0"] + 1, self.settings["heightBarline0Extension"], start, rectangle=True)
                self._plotDots(offset, start)

            if type(barLine) == music21.bar.Barline and barLine.type == 'final':

                self.plotVBar(offset, self.settings["lineWidth0"] + 1, self.settings["heightBarline0Extension"], start=False, rectangle=True)

            if type(barLine) == music21.bar.Barline and barLine.type == 'double':

                self.plotVBar(offset, self.settings["lineWidth0"], self.settings["heightBarline0Extension"], start=False, double=True)


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

    def plotVBar(self, offset, lineWidth, extension, start, rectangle=False, double=False):

        line, offsetLine = self.LocationFinder.getLocation(offset, start=start)
        page = self.CanvasCreator.getLinesToPage()[line]

        yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"]

        xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)

        if double:
            xPos -= 0.003

        if not rectangle:
            self.axs[page].vlines(xPos, yPosLow, yPosHigh + extension,
                              linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)
        else:
            width = 0.002
            if not start:
                xPos -= width
            patch = Rectangle((xPos, yPosLow), width=width, height=self.settings["yMax"] + extension - self.settings["yMin"], color='grey', fill=True)
            self.axs[page].add_patch(patch)

    def _plotDots(self, offset, start):
        line, offsetLine = self.LocationFinder.getLocation(offset, start=start)
        page = self.CanvasCreator.getLinesToPage()[line]

        yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"] + self.settings["heightBarline0Extension"]
        yPos = (yPosHigh + yPosLow)/2

        xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)

        shift = - 0.0065
        if start:
            shift = shift * -1

        xPos = xPos + shift

        for i in [-1, 1]:

            xyRatio =  self.settings["widthA4"] / self.settings["heightA4"]
            patch = Ellipse((xPos, yPos + i*0.005), width=0.003, height=0.003*xyRatio, color='grey')

            self.axs[page].add_patch(patch)

    def _plotRepeatBrackets(self, measure):
        if measure.getSpannerSites():
            spanner = measure.getSpannerSites()[0]
            if type(spanner) == music21.spanner.RepeatBracket:

                offset = measure.offset

                line, offsetLine = self.LocationFinder.getLocation(offset, start=True)
                page = self.CanvasCreator.getLinesToPage()[line]

                yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
                yPosHigh = yPosLineBase + self.settings["yMax"]  #TODO(add extension)

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


    def _plotRepeatExpressions(self, measure):

        for el in measure.recurse():

            if type(el).__module__ == 'music21.repeat' and music21.repeat.RepeatExpression in inspect.getmro(type(el)):

                offsetMeasure = measure.offset

                line, offsetLine = self.LocationFinder.getLocation(offsetMeasure)

                offsetLine += el.getOffsetInHierarchy(measure)
                xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine)

                yPosLineBase = self.CanvasCreator.getYPosLineBase(line)
                yPos = yPosLineBase + self.settings["yMax"] # + self.settings["heightBarline0Extension"]
                page = self.CanvasCreator.getLinesToPage()[line]


                if el.getOffsetInHierarchy(measure) < measure.duration.quarterLength * 0.5:
                    ha = 'left'
                    xPos += self.settings["xShiftChords"]
                else:
                    ha = 'right'
                    xPos -= self.settings["xShiftChords"]

                fp = fp1
                fontsize = 16
                if el.name == 'segno':
                    text = "𝄋"
                elif el.name == 'coda':
                    text = '𝄌'
                    fontsize=24
                else:
                    text = el.getText()
                    fp = fp2
                    fontsize = self.settings['fontSizeNotes']

                self.axs[page].text(xPos, yPos, text,
                                    fontsize=fontsize,
                                    fontproperties=fp,
                                    va='baseline', ha=ha)