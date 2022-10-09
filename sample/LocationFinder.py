import math

import music21


class LocationFinder:

    def __init__(self, streamObj, Settings):
        self.streamObj = streamObj
        self.Settings = Settings

        self.offsetsStartLine, self.xsStartLine = self._getOffsetsAndXsStartLine(Settings.offsetLineMax,)

        self.yMin = self.Settings.yMin
        self.yMax = self.Settings.yMax
        self.heightLine = self.yMax - self.yMin + Settings.vMarginLineTop

        self.offsetLineMax = Settings.offsetLineMax

        self.lengthPickupMeasure = self.getLengthPickupMeasure()

        self.linesToPage = []
        self.linesToLineOnPage = []

        self._divideLinesOverPages(self.getNumLines())

    def _getOffsetsAndXsStartLine(self, offsetLineMax):
        offsetsStartLine = []
        xsStartLine = []

        measures = self._getMeasures()
        hasPickupMeasure = measures[0].number == 0

        for measure in self.streamObj.recurse().getElementsByClass(music21.stream.Measure):

            if measure.number == 0:  # pickup measure
                offsetsStartLine.append(measure.offset)
                xsStartLine.append(-measure.quarterLength)

            elif measure.number == 1 and not hasPickupMeasure:
                offsetsStartLine.append(measure.offset)
                xsStartLine.append(0)

            # start new line when new section of song starts
            elif measure.flat.getElementsByClass(music21.expressions.RehearsalMark).first() and not measure.number == 1:
                offsetsStartLine.append(measure.offset)
                xsStartLine.append(0)

            elif measure.getSpannerSites():
                spanner = measure.getSpannerSites()[0]
                if type(spanner) == music21.spanner.RepeatBracket:
                    if int(spanner.number) > 1:
                        if spanner.isFirst(measure):
                            offsetsStartLine.append(measure.offset)
                            xsStartLine.append(xPosSpanner)

            if measure.offset + measure.quarterLength - offsetsStartLine[-1] + xsStartLine[-1] > offsetLineMax:
                offsetsStartLine.append(measure.offset)
                xsStartLine.append(0)

            if measure.getSpannerSites():
                spanner = measure.getSpannerSites()[0]
                if type(spanner) == music21.spanner.RepeatBracket:
                    if spanner.number == '1':
                        if spanner.isFirst(measure):
                            xPosSpanner = measure.offset - offsetsStartLine[-1] + xsStartLine[-1]

            # will not work if length of measure exceeds offsetLineMax, then will be counted in first and last (el)if statement

        return offsetsStartLine, xsStartLine

    def _divideLinesOverPages(self, numLines):
        pageIndex = 0
        isFirstPage = True
        numLinesToMake = numLines
        while numLinesToMake > 0:
            numLinesPage = min(self._getNumLinesPageMax(isFirstPage), numLinesToMake)
            numLinesToMake -= numLinesPage
            self.linesToLineOnPage += [LineOnPage for LineOnPage in range(numLinesPage)]
            self.linesToPage += [pageIndex for _ in range(numLinesPage)]
            isFirstPage = False  # TODO Use pageIndex
            pageIndex += 1
            if numLinesPage == 0:
                print("ax too big")
                break

    def _getNumLinesPageMax(self, isFirstPage):
        """returns the number of lines that fits on the page"""
        if isFirstPage:
            return math.floor((1 - self.Settings.yLengthTitleAx - self.Settings.vMarginBottomMinimal) / self.heightLine)
        else:
            return math.floor((1 - self.Settings.vMarginFirstLineTop - self.Settings.vMarginBottomMinimal) / self.heightLine)


    def _getMeasures(self):
        p = music21.graph.plot.PlotStream(self.streamObj)
        offsetMap = music21.graph.axis.OffsetAxis(p, 'x').getOffsetMap()
        measures = [measure[0] for measure in offsetMap.values()]
        return measures

    def _getLineAndOffsetLine(self, offset, start=True):
        """ returns a tuple (line, x) given an offset"""
        line = 0
        for idx, offsetStartLine in enumerate(self.offsetsStartLine):
            if start and offset >= offsetStartLine:
                line = idx
            elif (not start) and offset > offsetStartLine:
                line = idx
            else:
                break

        x = offset - self.offsetsStartLine[line] + self.xsStartLine[line]

        return line, x

    def getNumLines(self):
        return len(self.offsetsStartLine)

    def getLengthPickupMeasure(self):
        return - self.xsStartLine[0]

    # unused?
    def getXMax(self):
        if len(self.offsetsStartLine) > 1:
            return self.offsetsStartLine[1] - self.getLengthPickupMeasure()
        else:
            return self.streamObj.duration.quarterLength - self.getLengthPickupMeasure()

    def getLinesToPage(self):
        return self.linesToPage

    def getLinesToLineOnPage(self, linesToLineOnPage):
        return self.linesToLineOnPage

    # these functions could be moved to a general plotter class?

    def getYPosLineBase(self, line):
        heightLine = self.Settings.yMax - self.Settings.yMin
        yPosLineBase = 1 - self.linesToLineOnPage[line] * self.heightLine - self.Settings.yMax - self.Settings.vMarginLineTop
        if self.linesToPage[line] == 0:
            yPosLineBase -= self.Settings.yLengthTitleAx
        else:
            yPosLineBase -= self.Settings.vMarginFirstLineTop
        return yPosLineBase

    def _getPickupMeasureSpace(self):
        xPickupMeasureSpace = max(self.lengthPickupMeasure, self.Settings.xMinimalPickupMeasureSpace)

        return xPickupMeasureSpace

    def getXLengthFromOffsetLength(self, offsetLength):

        offsetLengthLine = self.offsetLineMax + 2 * self._getPickupMeasureSpace()

        plotSpace = 1 - 2 * self.Settings.widthMarginLine

        xPerOffset = plotSpace / offsetLengthLine

        xLength = offsetLength * xPerOffset

        return xLength

    def getXPosFromOffsetLine(self, offsetLine):
        xPos = self.Settings.widthMarginLine + self.getXLengthFromOffsetLength(
            (self._getPickupMeasureSpace() + offsetLine))

        return xPos

    def getLocation(self, offset, start=True):

        line, offsetLine = self._getLineAndOffsetLine(offset, start)
        yPosLineBase = self.getYPosLineBase(line)
        page = self.linesToPage[line]
        xPos = self.getXPosFromOffsetLine(offsetLine)

        return page, yPosLineBase, xPos

    def getNumPages(self):
        return len(self.linesToPage)
