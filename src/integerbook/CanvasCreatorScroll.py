import matplotlib.font_manager as font_manager
from matplotlib import rcParams
import matplotlib

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
from matplotlib.figure import Figure

class CanvasCreator:
    def __init__(self, Settings, numMeasures):

        self.Settings = Settings

        rcParams['mathtext.fontset'] = 'cm'

        matplotlib.use('Agg')

        self.yMin = self.Settings.yMin
        self.yMax = self.Settings.yMax

        self.figs = []
        self.axs = []

        self.numA4Widths = numMeasures / self.Settings.measuresPerLine

        self.widthA4 = self.Settings.widthA4
        self.heightA4 = self.Settings.heightA4


        self._createCanvas()

    def saveFig(self, pathName, maxXPos):

        yPosLowest = 1 - (self.yMax - self.yMin + 2 * self.Settings.vMarginLineTop)
        heightStart = self.heightA4 * yPosLowest

        xPosHighest = maxXPos + 2 * 0.01
        widthEnd = self.widthA4 * xPosHighest

        bbox = Bbox([[0, heightStart], [widthEnd, self.heightA4]])

        self.figs[0].savefig(pathName, dpi=self.Settings.dpi, bbox_inches=bbox, transparent=True)

    def _createCanvas(self):

        fig = Figure(figsize=(self.numA4Widths * self.widthA4, self.heightA4))
        ax = fig.subplots()
        ax = self._formatAx(ax)
        self.figs.append(fig)
        self.axs.append(ax)

    def _formatAx(self, ax):
        ax.set_ylim(0, 1)
        ax.set_xlim(0, self.numA4Widths)
        ax.axis('off')
        ax.set_position([0, 0, 1, 1])
        return ax

    def getAxs(self):
        return self.axs

    def getFigs(self):
        return self.figs

