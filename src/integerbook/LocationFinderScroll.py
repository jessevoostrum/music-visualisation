import math

import music21


class LocationFinder:

    def __init__(self, streamObj, Settings):
        self.streamObj = streamObj
        self.Settings = Settings

        self.offsetsStartLine = [0]

    def getLocation(self, offset, start=True):
        print(offset)
        yPosLineBase = self.getYPosLineBase(0)
        page = 0
        xPos = self._getXPosFromOffsetLine(offset)

        return page, yPosLineBase, xPos


    def getYPosLineBase(self, _):
        yPosLineBase = 1 - self.Settings.yMax - self.Settings.vMarginLineTop
        return yPosLineBase

    def getMaxXPos(self):
        offsetLengthSong = self.streamObj.duration.quarterLength
        print(offsetLengthSong)
        print(self._getXPosFromOffsetLine(offsetLengthSong))
        return self._getXPosFromOffsetLine(offsetLengthSong)

    def _getXPosFromOffsetLine(self, offsetLine):
        xPos = self._getXLengthFromOffsetLength(offsetLine) + 0.01
        return xPos

    def _getXLengthFromOffsetLength(self, offsetLength):
        defaultOffsetLengthLine = self.Settings.offsetLineMax + 2 * self.Settings.xMinimalPickupMeasureSpace
        plotSpace = 1 - 2 * self.Settings.widthMarginLine
        xPerOffset = plotSpace / defaultOffsetLengthLine
        xLength = offsetLength * xPerOffset
        return xLength





