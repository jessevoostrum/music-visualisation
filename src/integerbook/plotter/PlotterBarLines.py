import os
import inspect
import music21
from matplotlib.patches import Ellipse, Rectangle
import numpy as np
from contextlib import nullcontext
import matplotlib.pyplot as plt

from integerbook.plotter.patches import Segno, relativeWidthSegno, Coda

from integerbook.plotter.PlotterBase import Plotter

class PlotterBarLines(Plotter):

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        super().__init__(streamObj, Settings, LocationFinder, axs)

        self.spannedMeasures = self._getSpannedMeasures()

    def plotBarLines(self):

        if self.Settings.xkcd:
            context = plt.xkcd(scale=0.4, length=200, randomness=0)
        else:
            context = nullcontext()

        with context:

            measures = self.streamObj[music21.stream.Measure]

            for measure in measures:

                self._plotMeasureBarlines(measure)

                self._plotSubdivisions(measure)

                self._plotThickBarlines(measure)

                self._plotRepeatBrackets(measure)
                self._plotRepeatExpressions(measure)

                self._plotTimeSignature(measure)

                self._plotKey(measure)

    def _plotMeasureBarlines(self, measure):

        if not measure.number == 0:

            if self.isFirstNotPickUpMeasureOfLine(measure) and (not self.hasRepatBarline(
                    measure, 'start') or not self.Settings.thickBarlines):
                self._plotVLine(measure.offset, self.Settings.lineWidth0, self.Settings.heightBarline0Extension, start=True)

            if not self.hasRepatBarline(measure, 'end'):
                offsetEndMeasure = measure.offset + measure.quarterLength
                self._plotVLine(offsetEndMeasure, self.Settings.lineWidth0, self.Settings.heightBarline0Extension,
                                start=False)

    def hasRepatBarline(self, measure, direction):
        for barline in measure[music21.bar.Barline]:
            offset = measure.offset + barline.offset
            if type(barline) == music21.bar.Repeat:
                if barline.direction == direction:
                    return True
        return False

    def isFirstNotPickUpMeasureOfLine(self, measure):
        return measure.offset in self.LocationFinder.offsetsStartLine or measure.number == 1

    def _plotSubdivisions(self, measure):
        if self.Settings.subdivision == 1:
            self._plotSubdivisionBarLines(measure, 1, self.Settings.lineWidth2)

        elif self.Settings.subdivision == 2:
            self._plotSubdivisionBarLines(measure, 1, self.Settings.lineWidth1)
            self._plotSubdivisionBarLines(measure, 0.25, self.Settings.lineWidth2)

    def _plotSubdivisionBarLines(self, measure, step, lineWidth):

        for t in np.arange(0, measure.quarterLength, step=step)[1:]:
            if measure.number == 0:
                offset = measure.offset + measure.quarterLength - t
            elif measure.number >= 1:
                offset = measure.offset + t

            self._plotVLine(offset, lineWidth, 0, True)

    def _plotThickBarlines(self, measure):

        # these barLines are plotted on top of the "normal" barLines

        if self.Settings.thickBarlines:

            for barLine in measure[music21.bar.Barline]:
                offset = measure.offset + barLine.offset

                if type(barLine) == music21.bar.Repeat:
                    self._plotRepeatBarLine(barLine, offset)

                if type(barLine) == music21.bar.Barline and barLine.type == 'final':
                    self._plotThickVLine(offset, self.Settings.heightBarline0Extension, start=False)

                if type(barLine) == music21.bar.Barline and barLine.type == 'double' and measure.number != 0:
                    self._plotVLine(offset - .1, self.Settings.lineWidth0, self.Settings.heightBarline0Extension, start=False)

    def _plotRepeatBarLine(self, barLine, offset):

        if barLine.direction == 'start':
            start = True
        else:
            start = False

        self._plotThickVLine(offset, self.Settings.heightBarline0Extension, start, repeat=True)
        self._plotDots(offset, start)
        self._plotHBar(offset, start)

    def _plotVLine(self, offset, lineWidth, extension, start):

        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin

        xPos -= 0.5 * lineWidth

        patch = Rectangle((xPos, yPosLow), width=lineWidth, height=self.Settings.yMax + extension - self.Settings.yMin,
                          color=self.Settings.colorBarlines, fill=True,
                          zorder=.4,
                          linewidth=0
                          )
        self.axs[page].add_patch(patch)

    def _plotThickVLine(self, offset, extension, start, repeat=False):

        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin

        lineWidth = self.Settings.widthThickBarline

        if start:
            xPos -= 0.5 * self.Settings.lineWidth0

        if not start:
            xPos += 0.5 * self.Settings.lineWidth0 - lineWidth

        if not repeat:
            patch = Rectangle((xPos, yPosLow), width=lineWidth, height=self.Settings.yMax + extension - self.Settings.yMin,
                              color=self.Settings.colorBarlines, fill=True,
                              zorder=.4,
                              linewidth=0
                              )
            self.axs[page].add_patch(patch)

        else:

            lineHeightTotal = self.Settings.yMax + extension - self.Settings.yMin
            ySpaceDots = 0.033

            lineHeight = lineHeightTotal / 2 - ySpaceDots / 2

            patch = Rectangle((xPos, yPosLow), width=lineWidth, height=lineHeight,
                              color=self.Settings.colorBarlines, fill=True, zorder=.4, linewidth=0)
            self.axs[page].add_patch(patch)

            patch = Rectangle((xPos, yPosLow + lineHeight + ySpaceDots), width=lineWidth, height=lineHeight,
                              color=self.Settings.colorBarlines, fill=True, zorder=.4, linewidth=0)
            self.axs[page].add_patch(patch)




    def _plotDots(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin
        yPosHigh = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension
        yPos = (yPosHigh + yPosLow)/2

        xShiftThickBarline = 0.5 * self.Settings.lineWidth0
        xShiftCenterDot = 0.5 * self.Settings.widthThickBarline - xShiftThickBarline
        if start:
            shift = xShiftCenterDot
        else:
            shift = -xShiftCenterDot

        xPos = xPos + shift

        for i in [-1, 1]:

            distance = 0.007
            xyRatio = self.Settings.widthA4 / self.Settings.heightA4
            patch = Ellipse((xPos, yPos + i*distance), width=self.Settings.widthThickBarline,
                            height=self.Settings.widthThickBarline*xyRatio, color=self.Settings.colorBarlines, linewidth=0)

            self.axs[page].add_patch(patch)


    def _plotHBar(self, offset, start):
        page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start)

        yPosLow = yPosLineBase + self.Settings.yMin
        yPosHigh = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension

        width = 0.008

        if not start:
            xPos -= width

        for yPos in [yPosLow, yPosHigh - self.Settings.widthThickBarline]:
            patch = Rectangle((xPos, yPos), height=self.Settings.widthThickBarline, width=width,
                              color=self.Settings.colorBarlines, linewidth=0)
            self.axs[page].add_patch(patch)

    def _plotRepeatBrackets(self, measure):
        if measure.number in self.spannedMeasures:
            spanner = self.spannedMeasures[measure.number]
            offset = measure.offset

            page, yPosLineBase, xPosStart = self.LocationFinder.getLocation(offset, start=True)

            yPosHigh = yPosLineBase + self.Settings.yMax  #TODO(add extension)

            xPosEnd = xPosStart + self.LocationFinder._getXLengthFromOffsetLength(measure.quarterLength)

            lineWidth = 1
            self.axs[page].hlines(yPosHigh + 0.02, xPosStart - self.Settings.lineWidth0/2, xPosEnd,
                                  linestyle='dotted', linewidth=lineWidth, color=self.Settings.colorBarlines, zorder=.5)

            if spanner.isFirst(measure):
                number = spanner.number + "."
                self.axs[page].text(xPosStart + 0.0055, yPosHigh + self.Settings.heightBarline0Extension,  number, color=self.Settings.colorBarlines)

                self.axs[page].vlines(xPosStart, yPosHigh + 0.01, yPosHigh + 0.02,
                                      linestyle='dotted', linewidth=lineWidth, color=self.Settings.colorBarlines, zorder=.5)

            if spanner.isLast(measure):
                # self.axs[page].vlines(xPosEnd, yPosHigh + 0.01, yPosHigh + 0.02,
                #                       linestyle='solid', linewidth=lineWidth, color='grey', zorder=.5)

                pass

    def _plotRepeatExpressions(self, measure):

        for el in measure.recurse():

            if self._isRepeatExpression(el):

                offset = measure.offset

                page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start=True)

                xPos += self.LocationFinder._getXLengthFromOffsetLength(el.getOffsetInHierarchy(measure))

                yPos = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension - self.Settings.capsizeNote


                if el.getOffsetInHierarchy(measure) < measure.duration.quarterLength * 0.5:
                    xPos += self.Settings.xShiftChords
                    alignRight = False
                    ha = 'left'
                else:
                    xPos -= self.Settings.xShiftChords
                    alignRight = True
                    ha = 'right'

                if el.name == 'segno':
                    self._plotSegno(xPos, yPos, page, alignRight)
                elif el.name == 'coda':
                    self._plotCoda(xPos, yPos, page, alignRight)
                else:
                    text = el.getText()
                    self.axs[page].text(xPos, yPos, text,
                                        fontsize=self.Settings.fontSizeNotes,
                                        ha=ha, va='baseline', color=self.Settings.colorBarlines)
    def _plotSegno(self, xPos, yPos, page, alignRight=True):
        xyRatio = self.Settings.widthA4 / self.Settings.heightA4
        height = self.Settings.capsizeNote
        width = height / xyRatio * relativeWidthSegno()
        if alignRight:
            xPos -= width

        patches = Segno(xPos, yPos, height, xyRatio, color=self.Settings.colorTextMelody)
        for patch in patches:
            self.axs[page].add_patch(patch)


    def _plotCoda(self, xPos, yPos, page, alignRight=True):

        xyRatio = self.Settings.widthA4 / self.Settings.heightA4

        height = self.Settings.capsizeNote
        width = height / xyRatio * .85

        if alignRight:
            xPos -= width

        patches = Coda(xPos, yPos, height, width, xyRatio, color=self.Settings.colorTextMelody)
        for patch in patches:
            self.axs[page].add_patch(patch)

    def _plotKey(self, measure):
        for i, key in enumerate(measure[music21.key.Key, music21.key.KeySignature]):
            if measure == self.streamObj[music21.stream.Measure][0] and i == 0 and not self.Settings.plotFirstKeyWithinBar:  # can key change halfway measure?
                continue

            offset = key.getOffsetInHierarchy(self.streamObj)

            if measure.number == 0:
                measureInWhichKeyIsPlotted = self.streamObj[music21.stream.Measure][1]
                offset = measureInWhichKeyIsPlotted.getOffsetInHierarchy(self.streamObj)
            else:
                measureInWhichKeyIsPlotted = measure


            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset, start=True)
            yPos = yPosLineBase + self.Settings.yMax #+ self.Settings.heightBarline0Extension - self.Settings.capsizeNote

            xPos += self.Settings.xShiftChords
            if self._hasRepeatExpressionAtStart(measureInWhichKeyIsPlotted):
                xPos += self.Settings.fontWidthNote * 2

            key = self.getKey(offset)
            letter = self._getKeyLetter(key)
            self.axs[page].text(xPos, yPos,
                                f"1 = {letter}",
                                fontsize=self.Settings.fontSizeNotes,
                                va='baseline', ha='left', color=self.Settings.colorTextKey)


    def _plotTimeSignature(self, measure):

        if self.Settings.plotTimeSignature:

            measures = self.streamObj[music21.stream.Measure]
            if measure.number == 0 and len(measures) > 1:
                firstMeasure = measures[1]
            else:
                firstMeasure = measure

            if self.Settings.timeSignatureWithBarlines:

                if self.Settings.subdivision == 0:

                    if measure[music21.meter.TimeSignature]:
                        if measure.number == 0:
                            measure = firstMeasure
                        self._plotSubdivisionBarLines(measure, 1, self.Settings.lineWidth2)

            else:
                if measure[music21.meter.TimeSignature]:

                    ts = measure[music21.meter.TimeSignature][0]
                    ts = f"{ts.numerator}/{ts.denominator}"

                    if measure.number == 0:
                        measure = firstMeasure

                    page, yPosLineBase, xPos = self.LocationFinder.getLocation(measure.offset, start=True)

                    xPos += self.LocationFinder._getXLengthFromOffsetLength(measure.quarterLength / 2)

                    yPos = yPosLineBase + self.Settings.yMax + self.Settings.heightBarline0Extension - self.Settings.capsizeNote

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

    def _hasRepeatExpressionAtStart(self, measure):
        for el in measure.recurse():
            if self._isRepeatExpression(el):
                if el.name == 'segno' or el.name == 'coda':
                    return True

        return False

    def _isRepeatExpression(self, el):
        return type(el).__module__ == 'music21.repeat' and music21.repeat.RepeatExpression in inspect.getmro(type(el))
