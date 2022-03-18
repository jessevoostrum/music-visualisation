import math

import matplotlib.pyplot as plt


class CanvasCreator:
    def __init__(self, numLines, yMin, yMax):

        self.widthA4 = 8.27
        self.heightA4 = 11.69

        # below heights are given relative to height of the page
        self.heightMarginLine = 0.02  # above the line (page margins can make sure that there is a margin at the bottom)

        self.yMin = yMin
        self.yMax = yMax
        self.heightAxs = self.yMax - self.yMin

        self.figs, self.axs = self._createCanvas(numLines)

    def _createCanvas(self, numAxsToMake):

        figs = []
        axs = []

        while numAxsToMake > 0:
            fig = plt.figure(figsize=(self.widthA4, self.heightA4))
            numLinesFig = min(self._getNumLinesPage(), numAxsToMake)
            axsFig = fig.subplots(numLinesFig, sharex=True, squeeze=False)
            figs.append(fig)
            axs.append(list(axsFig[:, 0]))
            numAxsToMake -= numLinesFig

        # format axes
        for j, axsFig in enumerate(axs):
            for i, ax in enumerate(axsFig):
                ax.set_ylim(self.yMin, self.yMax)
                ax.axis('off')

                vPos = 1 - (i + 1) * (self.heightAxs + self.heightMarginLine)

                ax.set_position([0, vPos, 1, self.heightAxs])

        return figs, axs

    def _getNumLinesPage(self):
        """returns the number of lines that fits on the page"""
        return math.floor(1 / (self.heightAxs + self.heightMarginLine))

    def getAxs1D(self):
        return [ax for axsFig in self.axs for ax in axsFig]
