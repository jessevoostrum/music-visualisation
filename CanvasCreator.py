"""
summary:
- associate lines to pages
- give every line a location on the page
"""


import math

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rcParams

# Add every font at the specified location
font_dir = ['/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/OH no Type Company Order #e6cd109/Vulf Mono/Desktop']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# Set font family globally
rcParams['font.family'] = 'Vulf Mono'
rcParams['font.style'] = 'italic'
rcParams['font.weight'] = 'light'



class CanvasCreator:
    def __init__(self, settings, numLines, lengthPickupMeasure):

        self.settings = settings

        self.yMin = self.settings["yMin"]
        self.yMax = self.settings["yMax"]
        self.heightAxs = self.yMax - self.yMin + settings["vMarginLineTop"]

        self.offsetLineMax = settings["offsetLineMax"]

        self.lengthPickupMeasure = lengthPickupMeasure

        self.figs = []
        self.axs = []
        self.linesToPage = []
        self.linesToLineOnPage = []

        self._createCanvas(numLines)

    def _createCanvas(self, numLines):

        pageIndex = 0
        isFirstPage = True
        numLinesToMake = numLines
        while numLinesToMake > 0:
            fig, ax = plt.subplots(figsize=(self.settings["widthA4"], self.settings["heightA4"]))
            ax = self._formatAx(ax)
            self.figs.append(fig)
            self.axs.append(ax)
            numLinesPage = min(self._getNumLinesPageMax(isFirstPage), numLinesToMake)
            numLinesToMake -= numLinesPage
            self.linesToLineOnPage += [LineOnPage for LineOnPage in range(numLinesPage)]
            self.linesToPage += [pageIndex for _ in range(numLinesPage)]
            isFirstPage = False   # TODO Use pageIndex
            pageIndex += 1
            if numLinesPage == 0:
                print("ax too big")
                break

    def _formatAx(self, ax):
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)
        ax.axis('off')
        ax.set_position([0, 0, 1, 1])
        return ax

    def _getNumLinesPageMax(self, isFirstPage):
        """returns the number of lines that fits on the page"""
        if isFirstPage:
            return math.floor((1 - self.settings["yLengthTitleAx"] - self.settings["vMarginBottomMinimal"]) / self.heightAxs)
        else:
            return math.floor((1 - self.settings["vMarginFirstLineTop"] - self.settings["vMarginBottomMinimal"]) / self.heightAxs)

    def getAxs(self):
        return self.axs

    def getFigs(self):
        return self.figs

    def getLinesToLineOnPage(self):
        return self.linesToLineOnPage

    def getLinesToPage(self):
        return self.linesToPage


    # these functions could be moved to a general plotter class?

    def getYPosLineBase(self, line):
        heightLine = self.settings["yMax"] - self.settings["yMin"]
        yPosLineBase = 1 - self.linesToLineOnPage[line] * (heightLine + self.settings["vMarginLineTop"]) - self.settings["yMax"]
        if self.linesToPage[line] == 0:
            yPosLineBase -= self.settings["yLengthTitleAx"]
        else:
            yPosLineBase -= self.settings["vMarginFirstLineTop"]
        return yPosLineBase


    def _getPickupMeasureSpace(self):
        xPickupMeasureSpace = max(self.lengthPickupMeasure, self.settings["xMinimalPickupMeasureSpace"])

        return xPickupMeasureSpace


    def getXLengthFromOffsetLength(self, offsetLength):

        offsetLengthLine = self.offsetLineMax + 2 * self._getPickupMeasureSpace()

        plotSpace = 1 - 2 * self.settings["widthMarginLine"]

        xPerOffset = plotSpace / offsetLengthLine

        xLength = offsetLength * xPerOffset

        return xLength


    def getXPosFromOffsetLine(self, offsetLine):
        xPos = self.settings["widthMarginLine"] + self.getXLengthFromOffsetLength((self._getPickupMeasureSpace() + offsetLine))

        return xPos
