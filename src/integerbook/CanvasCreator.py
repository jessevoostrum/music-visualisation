import matplotlib.font_manager as font_manager
from matplotlib import rcParams

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
from matplotlib.figure import Figure

class CanvasCreator:
    def __init__(self, Settings, numPages, yPosLowest):

        self.Settings = Settings

        fontDir = self.Settings.fontDirectory
        if fontDir:
            for font in font_manager.findSystemFonts(fontDir):
                font_manager.fontManager.addfont(font)

        # Set font family globally
        rcParams['font.family'] = self.Settings.font
        rcParams['font.style'] = self.Settings.fontStyle
        rcParams['font.weight'] = self.Settings.fontWeight
        rcParams['mathtext.fontset'] = 'cm'

        self.yMin = self.Settings.yMin
        self.yMax = self.Settings.yMax
        self.heightLine = self.yMax - self.yMin + Settings.vMarginLineTop

        self.offsetLineMax = Settings.offsetLineMax

        self.figs = []
        self.axs = []

        self._createCanvas(numPages)

        self.yPosLowest = yPosLowest



    def saveFig(self, pathName):

        with PdfPages(pathName) as pdf:
            for fig in self.figs:
                yLengthAboveTitle = 1 - self.Settings.yPosTitle
                if len(self.figs) == 1 and self.yPosLowest >= 0.55 and self.Settings.saveCropped:
                    heightStart = self.Settings.heightA4 * (self.yPosLowest - yLengthAboveTitle)
                    bbox = Bbox([[0, heightStart], [self.Settings.widthA4, self.Settings.heightA4]])
                    pdf.savefig(fig, bbox_inches=bbox)
                else:
                    pdf.savefig(fig)

    def _createCanvas(self, numPages):

        for _ in range(numPages):

            fig = Figure(figsize=(self.Settings.widthA4, self.Settings.heightA4))
            ax = fig.subplots()
            ax = self._formatAx(ax)
            self.figs.append(fig)
            self.axs.append(ax)

    def _formatAx(self, ax):
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)
        ax.axis('off')
        ax.set_position([0, 0, 1, 1])
        return ax

    def getAxs(self):
        return self.axs

    def getFigs(self):
        return self.figs

