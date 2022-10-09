"""
summary:
- associate lines to pages
- give every line a location on the page
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rcParams

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox

# Add every font at the specified location
font_dir = ['/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/OH no Type Company Order #e6cd109/Vulf Mono/Desktop']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# Set font family globally
rcParams['font.family'] = 'Vulf Mono'
rcParams['font.style'] = 'italic'
rcParams['font.weight'] = 'light'



class CanvasCreator:
    def __init__(self, Settings, numPages):

        self.Settings = Settings

        self.yMin = self.Settings.yMin
        self.yMax = self.Settings.yMax
        self.heightLine = self.yMax - self.yMin + Settings.vMarginLineTop

        self.offsetLineMax = Settings.offsetLineMax

        self.figs = []
        self.axs = []

        self._createCanvas(numPages)

    def saveFig(self, title, pathName, yPosLowest):

        with PdfPages(pathName) as pdf:
            for fig in self.figs:
                yLengthAboveTitle = 1 - self.Settings.yPosTitle
                if len(self.figs) == 1 and yPosLowest >= 0.55:
                    heightStart = self.Settings.heightA4 * (yPosLowest - yLengthAboveTitle)
                    bbox = Bbox([[0, heightStart], [self.Settings.widthA4, self.Settings.heightA4]])
                    pdf.savefig(fig, bbox_inches=bbox)
                else:
                    pdf.savefig(fig)

        plt.close("all")

    def _createCanvas(self, numPages):

        for _ in range(numPages):
            fig, ax = plt.subplots(figsize=(self.Settings.widthA4, self.Settings.heightA4))
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

