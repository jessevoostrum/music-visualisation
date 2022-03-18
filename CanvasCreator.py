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

        self._setXDimensionsMusic(lengthPickupMeasure)
        self._setXDimensionsTitle()

        self.figs = []
        self.axs = []

        self._createCanvas(numLines)

    def _createCanvas(self, numAxsToMake):

        self._createFigsAndMusicAxs(numAxsToMake)
        self._formatMusicAxs()
        self._createAndFormatTitleAx()

    def _createFigsAndMusicAxs(self, numAxsToMake):

        isFirstPage = True
        while numAxsToMake > 0:
            fig = plt.figure(figsize=(self.settings["widthA4"], self.settings["heightA4"]))
            numLinesFig = min(self._getNumLinesPage(isFirstPage), numAxsToMake)
            axsFig = fig.subplots(numLinesFig, sharex=True, squeeze=False)
            self.figs.append(fig)
            self.axs.append(list(axsFig[:, 0]))
            numAxsToMake -= numLinesFig
            isFirstPage = False
            if numLinesFig == 0:
                print("ax too big")
                break

    def _formatMusicAxs(self):
        isFirstPage = True
        for j, axsFig in enumerate(self.axs):
            for i, ax in enumerate(axsFig):
                ax.set_ylim(self.yMin, self.yMax + self.settings["vMarginLineTop"])
                ax.set_xlim(- self.xPickupMeasureSpacePlusMargin, self.xMax + self.xPickupMeasureSpacePlusMargin)

                ax.axis('off')

                vPosAx = 1 - (i + 1) * self.heightAxs
                if isFirstPage:
                    vPosAx += -self.heightTitleAx + self.settings["vMarginLineTop"] - self.settings["vMarginFirstLineTop"]

                ax.set_position([0, vPosAx, 1, self.heightAxs])
            isFirstPage = False

        self.vPosLowest = vPosAx

    def _createAndFormatTitleAx(self):
        titleAx = self.figs[0].subplots(1, squeeze=True)
        titleAx.axis("off")
        titleAx.set_position([0, 1 - self.heightTitleAx, 1, self.heightTitleAx])
        titleAx.set_xlim(- self.xPickupMeasureSpacePlusMarginTitle, self.xMax + self.xPickupMeasureSpacePlusMarginTitle)
        titleAx.set_ylim(0, 1)
        self.titleAx = titleAx

    def _getNumLinesPage(self, isFirstPage):
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

    def getAxs1D(self):
        return [ax for axsFig in self.axs for ax in axsFig]

    def getFigs(self):
        return self.figs

    def getWidthAx(self):
        return self.xLengthWithMargin

    def getVPosLowest(self):
        return self.vPosLowest