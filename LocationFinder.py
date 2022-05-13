import music21
import copy


class LocationFinder:

    def __init__(self, streamObj, offsetLineMax):
        self.streamObj = streamObj
        self.offsetsStartLine, self.xsStartLine = self._getOffsetsAndXsStartLine(offsetLineMax)

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

    def _getMeasures(self):
        p = music21.graph.plot.PlotStream(self.streamObj)
        offsetMap = music21.graph.axis.OffsetAxis(p, 'x').getOffsetMap()
        measures = [measure[0] for measure in offsetMap.values()]
        return measures

    def getLocation(self, offset, start=True):
        """ returns a tuple (line, x) given an offset"""

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
