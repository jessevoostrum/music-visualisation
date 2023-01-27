import os
import inspect
import music21
from matplotlib.patches import Ellipse, Rectangle
import matplotlib.font_manager as fm
import numpy as np

from sample.plotter.Plotter import Plotter

fontDirectory = os.path.join(os.path.dirname(__file__), '../fonts/')
fontPropertiesSymbola = fm.FontProperties(fname=fontDirectory + "symbola/Symbola.ttf")


class PlotterBarlines(Plotter):

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        super().__init__(streamObj, Settings, LocationFinder, axs)

        self.spannedMeasures = self._getSpannedMeasures()

    def plotBarlines(self):

        measures = self.streamObj[music21.stream.Measure]

        for measure in measures:

            self._plotMeasureBarlines(measure)

            if self.Settings.subdivision >= 1:
                self._plotSubdivisionBarlines(measure, 1, self.Settings.lineWidth1)

            if self.Settings.subdivision >= 2:
                self._plotSubdivisionBarlines(measure, 0.25, self.Settings.lineWidth2)

            self._plotRepeatBrackets(measure)
            self._plotRepeatExpressions(measure)

            if measure.number == 0 and len(measures) > 1:
                firstMeasure = self.streamObj.recurse().getElementsByClass(music21.stream.Measure)[1]
            else:
                firstMeasure = measure

            if self.Settings.subdivision == 0:
                self._plotTimeSignature(measure, firstMeasure)

            self._plotKey(measure)

    def _plotMeasureBarlines(self, measure):
        if not measure.number == 0:
            self._plotVBar(measure.offset, self.Settings.lineWidth0, self.Settings.heightBarline0Extension, start=True)

            offsetEndMeasure = measure.offset + measure.quarterLength
            self._plotVBar(offsetEndMeasure, self.Settings.lineWidth0, self.Settings.heightBarline0Extension, start=False)

        if self.Settings.thickBarlines:

            for barLine in measure[music21.bar.Barline]:
                offset = measure.offset + barLine.offset

                if type(barLine) == music21.bar.Repeat:

                    if barLine.direction == 'start':
                        start = True
                    else:
                        start = False

                    self._plotVBar(offset, self.Settings.lineWidth0 + 1, self.Settings.heightBarline0Extension, start,
                                   rectangle=True)
                    self._plotDots(offset, start)
                    self._plotHBar(offset, start)

                if type(barLine) == music21.bar.Barline and barLine.type == 'final':
                    self._plotVBar(offset, None, self.Settings.heightBarline0Extension, start=False, rectangle=True)

                if type(barLine) == music21.bar.Barline and barLine.type == 'double' and measure.number != 0:
                    self._plotVBar(offset, None, self.Settings.heightBarline0Extension, start=False, double=True)


    def _plotSubdivisionBarlines(self, measure, step, lineWidth):

        for t in np.arange(0, measure.quarterLength, step=step):
            if measure.number == 0:
                offset = measure.offset + measure.quarterLength - t
            elif measure.number >= 1:
                offset = measure.offset + t

            self._plotVBar(offset, lineWidth, 0, True)

    def _plotVBar(self, offset, lineWidth, extension, start, rectangle=False, double=False):

        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin
        yPosHigh = yPosLineBase + self.Settings.yMax

        if double:
            xPos -= 0.003

        if not rectangle:
            self.axs[page].vlines(xPos, yPosLow, yPosHigh + extension,
                              linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)
        else:
            width = self.Settings.widthThickBarline
            if not start:
                xPos -= width
            patch = Rectangle((xPos, yPosLow), width=width, height=self.Settings.yMax + extension - self.Settings.yMin, color='grey', fill=True, zorder=.5)
            self.axs[page].add_patch(patch)


    def _plotDots(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin
        yPosHigh = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension
        yPos = (yPosHigh + yPosLow)/2

        shift = - self.Settings.widthThickBarline * 0.5  # - 0.0065
        if start:
            shift = shift * -1
        xPos = xPos + shift

        for i in [-1, 1]:

            distance = 0.007
            xyRatio =  self.Settings.widthA4 / self.Settings.heightA4
            patch = Ellipse((xPos, yPos + i*distance), width=self.Settings.widthThickBarline, height=self.Settings.widthThickBarline*xyRatio, color='grey')

            self.axs[page].add_patch(patch)

        margin = 0.007
        patch = Rectangle((xPos - 0.5 * self.Settings.widthThickBarline - 0.0001, yPos - distance - margin),
                          width=self.Settings.widthThickBarline + 0.0002, height=2 * distance + 2 * margin, color='white', zorder=0.5)

        self.axs[page].add_patch(patch)

    def _plotHBar(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin
        yPosHigh = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension

        width = 0.008

        if not start:
            xPos -= width

        for yPos in [yPosLow, yPosHigh - self.Settings.widthThickBarline]:
            patch = Rectangle((xPos, yPos), height=self.Settings.widthThickBarline, width=width, color='grey')
            self.axs[page].add_patch(patch)

    def _plotRepeatBrackets(self, measure):
        if measure.number in self.spannedMeasures:
            spanner = self.spannedMeasures[measure.number]
            offset = measure.offset

            page, yPosLineBase, xPosStart = self.LocationFinder.getLocation(offset, start=True)

            yPosHigh = yPosLineBase + self.Settings.yMax  #TODO(add extension)

            xPosEnd = xPosStart + self.LocationFinder._getXLengthFromOffsetLength(measure.quarterLength)

            lineWidth = self.Settings.lineWidth0
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

                xPos += self.LocationFinder._getXLengthFromOffsetLength(el.getOffsetInHierarchy(measure))

                yPos = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension - self.Settings.capsizeNumberNote


                if el.getOffsetInHierarchy(measure) < measure.duration.quarterLength * 0.5:
                    ha = 'left'
                    xPos += self.Settings.xShiftChords
                else:
                    ha = 'right'
                    xPos -= self.Settings.xShiftChords


                if el.name == 'segno':
                    text = "𝄋"
                    fontSize = self.Settings.fontSizeSegno
                    fontProperties = fontPropertiesSymbola
                    va = 'bottom'
                elif el.name == 'coda':
                    text = '𝄌'
                    fontSize = self.Settings.fontSizeCoda
                    fontProperties = fontPropertiesSymbola
                    va = 'bottom'
                else:
                    text = el.getText()
                    fontProperties = None  # this makes sure to use default font properties
                    fontSize = self.Settings.fontSizeNotes
                    va = 'baseline'

                self.axs[page].text(xPos, yPos, text,
                                    fontsize=fontSize,
                                    fontproperties=fontProperties,
                                    va=va, ha=ha)

    def _plotKey(self, measure):
        if measure[music21.key.Key, music21.key.KeySignature] and measure.number > 1:
            offset = measure.getOffsetInHierarchy(self.streamObj)
            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start=True)
            yPos = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension - self.Settings.capsizeNumberNote

            xPos += self.Settings.xShiftNumberNote
            key = self.Settings.getKey(offset)
            self.axs[page].text(xPos, yPos, f"1 = {self._getKeyLetter(key)} ", fontsize=self.Settings.fontSizeNotes,
                                va='baseline', ha='left')

    def _plotTimeSignature(self, measure, firstMeasure):

        if self.Settings.timeSignatureWithBarlines:

            if measure[music21.meter.TimeSignature]:
                if measure.number == 0:
                    measure = firstMeasure
                self._plotSubdivisionBarlines(measure, 1, self.Settings.lineWidth2)

        else:
            if measure[music21.meter.TimeSignature]:

                ts = measure[music21.meter.TimeSignature][0]
                ts = f"{ts.numerator}/{ts.denominator}"

                if measure.number == 0:
                    measure = firstMeasure

                page, yPosLineBase, xPos = self.LocationFinder.getLocation(measure.offset, start=True)

                xPos += self.LocationFinder._getXLengthFromOffsetLength(measure.quarterLength / 2)

                yPos = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension - self.Settings.capsizeNumberNote

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