import matplotlib.font_manager as font_manager
from matplotlib import rcParams

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
from matplotlib.figure import Figure

class CanvasCreator:
    def __init__(self, Settings, numPages, numMeasures):

        self.Settings = Settings

        self.yMin = self.Settings.yMin
        self.yMax = self.Settings.yMax
        self.heightLine = self.yMax - self.yMin + Settings.vMarginLineTop

        self.offsetLineMax = Settings.offsetLineMax

        self.figs = []
        self.axs = []

        if not self.Settings.scroll:
            self.numA4Widths = 1
        else:
            self.numA4Widths = numMeasures / self.Settings.measuresPerLine


        self._createCanvas(numPages)

    def saveFig(self, pathName, yPosLowest=0, maxXPos=1):

        if not self.Settings.scroll:
            with PdfPages(pathName) as pdf:
                for fig in self.figs:
                    yLengthAboveTitle = 1 - self.Settings.yPosTitle  # plotTitle has vertical alignment = top
                    if len(self.figs) == 1 and yPosLowest >= 0.55 and self.Settings.saveCropped:
                        heightStart = self.Settings.heightA4 * (yPosLowest - yLengthAboveTitle)
                        bbox = Bbox([[0, heightStart], [self.Settings.widthA4, self.Settings.heightA4]])
                        pdf.savefig(fig, bbox_inches=bbox)
                    else:
                        pdf.savefig(fig)

        else:
            yPosLowest = 1 - (self.yMax - self.yMin + 2 * self.Settings.vMarginLineTop)
            heightStart = self.Settings.heightA4 * yPosLowest

            xPosHighest = maxXPos + 2 * 0.01
            widthEnd = self.Settings.widthA4 * xPosHighest

            bbox = Bbox([[0, heightStart], [widthEnd, self.Settings.heightA4]])

            self.figs[0].savefig(pathName, dpi=self.Settings.dpi, bbox_inches=bbox, transparent=True)


    def _createCanvas(self, numPages):

        for _ in range(numPages):

            fig = Figure(figsize=(self.numA4Widths * self.Settings.widthA4, self.Settings.heightA4))
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

