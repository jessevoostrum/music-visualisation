import inspect
import music21
from matplotlib.patches import Ellipse, Rectangle
import matplotlib.font_manager as fm
import numpy as np

from sample.plotter.Plotter import Plotter


fp1=fm.FontProperties(fname="/Users/jvo/Downloads/freefont-20120503/FreeSerif.ttf")
fp1=fm.FontProperties(fname="/Users/jvo/Downloads/symbola/Symbola.ttf")

fp2=fm.FontProperties(fname="/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/OH no Type Company Order #e6cd109/Vulf Mono/Desktop/VulfMono-LightItalic.otf")

class PlotterBarlines(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):

        super().__init__(streamObj, settings, LocationFinder, axs)

        self.spannedMeasures = self._getSpannedMeasures()


    def plotBarlines(self):

        measures = self.streamObj[music21.stream.Measure]

        for measure in measures:

            self.plotMeasureBarlines(measure)

            if self.settings["subdivision"] >= 1:
                self.plotSubdivisionBarlines(measure, 1, self.settings["lineWidth1"])

            if self.settings["subdivision"] >= 2:
                self.plotSubdivisionBarlines(measure, 0.25, self.settings["lineWidth2"])

            self._plotRepeatBrackets(measure)
            self._plotRepeatExpressions(measure)

            if measure.number == 0 and len(measures) > 1:
                firstMeasure = self.streamObj.recurse().getElementsByClass(music21.stream.Measure)[1]
            else:
                firstMeasure = measure

            if self.settings["subdivision"] == 0:
                self._plotTimeSignature(measure, firstMeasure)

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
                self._plotHBar(offset, start)

            if type(barLine) == music21.bar.Barline and barLine.type == 'final':

                self.plotVBar(offset, None, self.settings["heightBarline0Extension"], start=False, rectangle=True)

            if type(barLine) == music21.bar.Barline and barLine.type == 'double' and measure.number != 0:

                self.plotVBar(offset, None, self.settings["heightBarline0Extension"], start=False, double=True)


    def plotSubdivisionBarlines(self, measure, step, lineWidth):

        for t in np.arange(0, measure.quarterLength, step=step):
            if measure.number == 0:
                offset = measure.offset + measure.quarterLength - t
            elif measure.number >= 1:
                offset = measure.offset + t

            self.plotVBar(offset, lineWidth, 0, True)

    def plotVBar(self, offset, lineWidth, extension, start, rectangle=False, double=False):

        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"]

        if double:
            xPos -= 0.003

        if not rectangle:
            self.axs[page].vlines(xPos, yPosLow, yPosHigh + extension,
                              linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)
        else:
            width = self.settings["widthThickBarline"]
            if not start:
                xPos -= width
            patch = Rectangle((xPos, yPosLow), width=width, height=self.settings["yMax"] + extension - self.settings["yMin"], color='grey', fill=True, zorder=.5)
            self.axs[page].add_patch(patch)


    def _plotDots(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"] + self.settings["heightBarline0Extension"]
        yPos = (yPosHigh + yPosLow)/2

        shift = - self.settings["widthThickBarline"] * 0.5  # - 0.0065
        if start:
            shift = shift * -1
        xPos = xPos + shift

        for i in [-1, 1]:

            distance = 0.007
            xyRatio =  self.settings["widthA4"] / self.settings["heightA4"]
            patch = Ellipse((xPos, yPos + i*distance), width=self.settings["widthThickBarline"], height=self.settings["widthThickBarline"]*xyRatio, color='grey')

            self.axs[page].add_patch(patch)

        margin = 0.007
        patch = Rectangle((xPos - 0.5 * self.settings["widthThickBarline"] - 0.0001, yPos - distance - margin),
                          width=self.settings["widthThickBarline"] + 0.0002, height=2 * distance + 2 * margin, color='white', zorder=0.5)

        self.axs[page].add_patch(patch)

    def _plotHBar(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.settings["yMin"]
        yPosHigh = yPosLineBase + self.settings["yMax"] + self.settings["heightBarline0Extension"]

        width = 0.008

        if not start:
            xPos -= width

        for yPos in [yPosLow, yPosHigh - self.settings["widthThickBarline"]]:
            patch = Rectangle((xPos, yPos), height=self.settings["widthThickBarline"], width=width, color='grey')
            self.axs[page].add_patch(patch)

    def _plotRepeatBrackets(self, measure):
        if measure.number in self.spannedMeasures:
            spanner = self.spannedMeasures[measure.number]
            offset = measure.offset

            page, yPosLineBase, xPosStart = self.LocationFinder.getLocation(offset, start=True)

            yPosHigh = yPosLineBase + self.settings["yMax"]  #TODO(add extension)

            xPosEnd = xPosStart + self.LocationFinder.getXLengthFromOffsetLength(measure.quarterLength)

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

                offset = measure.offset

                page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start=True)

                xPos += self.LocationFinder.getXLengthFromOffsetLength(el.getOffsetInHierarchy(measure))

                yPos = yPosLineBase + self.settings["yMax"] + self.settings["heightBarline0Extension"] - self.settings['capsizeNumberNote']


                if el.getOffsetInHierarchy(measure) < measure.duration.quarterLength * 0.5:
                    ha = 'left'
                    xPos += self.settings["xShiftChords"]
                else:
                    ha = 'right'
                    xPos -= self.settings["xShiftChords"]

                fp = fp1
                va = 'bottom'
                if el.name == 'segno':
                    text = "𝄋"
                    fontsize =  self.settings['fontSizeSegno']
                elif el.name == 'coda':
                    text = '𝄌'
                    fontsize = self.settings['fontSizeCoda']
                else:
                    text = el.getText()
                    fp = fp2
                    fontsize = self.settings['fontSizeNotes']
                    va = 'baseline'

                self.axs[page].text(xPos, yPos, text,
                                    fontsize=fontsize,
                                    fontproperties=fp,
                                    va=va, ha=ha)

    def _plotTimeSignature(self, measure, firstMeasure):

        if self.settings["timeSignatureWithBarlines"]:

            if measure[music21.meter.TimeSignature]:
                if measure.number == 0:
                    measure = firstMeasure
                self.plotSubdivisionBarlines(measure, 1, self.settings["lineWidth2"])

        else:
            if measure[music21.meter.TimeSignature]:

                ts = measure[music21.meter.TimeSignature][0]
                ts = f"{ts.numerator}/{ts.denominator}"

                if measure.number == 0:
                    measure = firstMeasure

                page, yPosLineBase, xPos = self.LocationFinder.getLocation(measure.offset, start=True)

                xPos += self.LocationFinder.getXLengthFromOffsetLength(measure.quarterLength / 2)

                yPos = yPosLineBase + self.settings["yMax"] + self.settings["heightBarline0Extension"] - self.settings['capsizeNumberNote']

                self.axs[page].text(xPos, yPos, ts,
                                    fontsize=10,
                                    va='baseline', ha='center')


    def _getSpannedMeasures(self):
        includedMeasuresDict = {}
        spanners = self.streamObj[music21.spanner.RepeatBracket]
        for sp in spanners:
            spannedMeasures = sp.getSpannedElements()
            measureNumberFirst = spannedMeasures[0].measureNumber
            measureNumberLast = spannedMeasures[-1].measureNumber

            for includedMeasure in np.arange(measureNumberFirst, measureNumberLast + 1):
                includedMeasuresDict[includedMeasure] = sp

        return includedMeasuresDict