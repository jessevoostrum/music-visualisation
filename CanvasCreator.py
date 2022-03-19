"""
to do:
- titleAx defined in method
- inititiate self.figs=[], self.axs=[] and let create_canvas fill them
- is it OK to introduce new attributes outside of init?
- rewrite setXdimensions. let it return a variable. better for testing?
- vPosAx not very nice
- numLines vs numAxToMake
"""


import math

import matplotlib.pyplot as plt
from matplotlib import rc


rc('text.latex', preamble=r'\usepackage{amssymb}')
plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": ['Computer Modern Sans serif']
        # "font.sans-serif": ['Helvetica']

})


class CanvasCreator:
    def __init__(self, settings, numLines, lengthPickupMeasure, yMin, yMax):

        self.settings = settings

        # below height and width are given relative to height and width of the page
        self.heightTitleAx = settings["heightTitleAx"]
        self.widthMarginLine = settings["widthMarginLine"]

        self.yMin = yMin
        self.yMax = yMax
        self.heightAxs = yMax - yMin + settings["vMarginLineTop"]

        self.xMax = settings["xMax"]

        self.lengthPickupMeasure = lengthPickupMeasure
        self.pickupMeasureSpace = self._calculatePickupMeasureSpace()

        self._setXDimensionsMusic(lengthPickupMeasure)
        self._setXDimensionsTitle()

        self.figs = []
        self.axs = []
        self.linesToPage = []
        self.linesToLineOnPage = []

        self._createCanvas(numLines)

    def _createCanvas(self, numLines):

        self._createFigsAndMusicAxs(numLines)
        self._formatMusicAxs()
        self._createAndFormatTitleAx()

    def _createFigsAndMusicAxs(self, numLines):

        pageIndex = 0
        isFirstPage = True
        numLinesToMake = numLines
        while numLinesToMake > 0:
            fig = plt.figure(figsize=(self.settings["widthA4"], self.settings["heightA4"]))
            axFig = fig.subplots()
            self.figs.append(fig)
            self.axs.append(axFig)
            numLinesPage = min(self._getNumLinesPageMax(isFirstPage), numLinesToMake)
            numLinesToMake -= numLinesPage
            self.linesToLineOnPage += [LineOnPage for LineOnPage in range(numLinesPage)]
            self.linesToPage += [pageIndex for _ in range(numLinesPage)]
            isFirstPage = False   # TODO Use pageIndex
            pageIndex += 1
            if numLinesPage == 0:
                print("ax too big")
                break

    def _formatMusicAxs(self):
        for ax in self.axs:
            ax.set_ylim(0, 1)
            # ax.set_xlim(- self.xPickupMeasureSpacePlusMargin, self.xMax + self.xPickupMeasureSpacePlusMargin)
            ax.set_xlim(0, 1)

            ax.axis('off')

            ax.set_position([0, 0, 1, 1])


    def _createAndFormatTitleAx(self):
        titleAx = self.figs[0].subplots(1, squeeze=True)
        titleAx.axis("off")
        titleAx.set_position([0, 1 - self.heightTitleAx, 1, self.heightTitleAx])
        titleAx.set_xlim(- self.xPickupMeasureSpacePlusMarginTitle, self.xMax + self.xPickupMeasureSpacePlusMarginTitle)
        titleAx.set_ylim(0, 1)
        self.titleAx = titleAx

    def _getNumLinesPageMax(self, isFirstPage):
        """returns the number of lines that fits on the page"""
        if isFirstPage:
            return math.floor((1 - self.heightTitleAx) / (self.heightAxs))
        else:
            return math.floor((1) / (self.heightAxs))

    def _setXDimensionsMusic(self, lengthPickupMeasure):
        xMinimalPickupMeasureSpace = self.xMax * self.settings["xMinimalPickupMeasureSpaceFraction"]

        xPickupMeasureSpace = max(lengthPickupMeasure, xMinimalPickupMeasureSpace)
        xLengthWithoutMargin = self.xMax + 2 * xPickupMeasureSpace

        xMargin = xLengthWithoutMargin * self.widthMarginLine / (1 - self.widthMarginLine)
        self.xPickupMeasureSpacePlusMargin = xPickupMeasureSpace + xMargin
        self.xLengthWithMargin = xLengthWithoutMargin + 2 * xMargin

    def _setXDimensionsTitle(self):
        # the composer location and key definition is always determined using the xMinimalPickupMeasureSpace
        # so that it is constant
        xMinimalPickupMeasureSpace = self.xMax * self.settings["xMinimalPickupMeasureSpaceFraction"]
        xLengthWithoutMarginTitle = self.xMax + 2 * xMinimalPickupMeasureSpace
        xMarginTitle = xLengthWithoutMarginTitle * self.widthMarginLine / (1 - self.widthMarginLine)
        self.xPickupMeasureSpacePlusMarginTitle = xMinimalPickupMeasureSpace + xMarginTitle

    def getTitleAx(self):
        return self.titleAx

    def getAxs(self):
        return self.axs

    def getFigs(self):
        return self.figs

    def getWidthAx(self):
        return self.xLengthWithMargin

    def getLinesToLineOnPage(self):
        return self.linesToLineOnPage

    def getLinesToPage(self):
        return self.linesToPage

    def getYPosLineBase(self, line):
        heightLine = self.settings["yMax"] - self.settings["yMin"]
        yPosLineBase = 1 - self.linesToLineOnPage[line] * (heightLine + self.settings["vMarginLineTop"]) - self.settings["yMax"]
        if self.linesToPage[line] == 0:
            yPosLineBase -= self.settings["heightTitleAx"]
        else:
            yPosLineBase -= self.settings["vMarginLineTop"]
        return yPosLineBase


    def _calculatePickupMeasureSpace(self):
        xMinimalPickupMeasureSpace = self.xMax * self.settings["xMinimalPickupMeasureSpaceFraction"]

        xPickupMeasureSpace = max(self.lengthPickupMeasure, xMinimalPickupMeasureSpace)

        return xPickupMeasureSpace


    def getXLengthFromOffsetLength(self, offsetLength):

        offsetLengthLine = self.xMax + 2 * self.pickupMeasureSpace

        plotSpace = 1 - 2 * self.settings["widthMarginLine"]

        xPerOffset = plotSpace / offsetLengthLine

        xLength = offsetLength * xPerOffset

        return xLength


    def getXPosFromOffsetLine(self, offsetLine):
        xPos = self.settings["widthMarginLine"] + self.getXLengthFromOffsetLength((self.pickupMeasureSpace + offsetLine))

        return xPos
