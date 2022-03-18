import music21


class LocationFinder:

    def __init__(self, streamObj, measuresPerLine):
        self.streamObj = streamObj
        self.offsetsStartLine = self._getTimesStartLine(measuresPerLine)

    def _getTimesStartLine(self, measuresPerLine):
        offsetsStartLine = []

        p = music21.graph.plot.PlotStream(self.streamObj)
        offsetMap = music21.graph.axis.OffsetAxis(p, 'x').getOffsetMap()

        offsetsStartMeasureDict = {measure[0].number: measure[0].offset for measure in offsetMap.values()}

        measureCounter = 0

        for measure in offsetsStartMeasureDict.keys():  # no support for pickup measures or repetitions

            if measureCounter == 0:
                offsetsStartLine.append(offsetsStartMeasureDict.get(measure))

            measureCounter += 1

            if measureCounter == measuresPerLine:
                measureCounter = 0

        return offsetsStartLine

    def getLocation(self, offset):
        """ returns a tuple (line, x) given an offset"""

        for idx, offsetStartLine in enumerate(self.offsetsStartLine):
            if offset >= offsetStartLine:
                line = idx
            else:
                break

        x = offset - self.offsetsStartLine[line]

        return line, x

    def getNumLines(self):
        """return num lines"""
        return len(self.offsetsStartLine)