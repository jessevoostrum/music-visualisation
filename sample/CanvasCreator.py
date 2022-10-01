"""
summary:
- associate lines to pages
- give every line a location on the page
"""

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
    def __init__(self, settings, LocationFinder):

        self.settings = settings
        self.LocationFinder = LocationFinder

        self.yMin = self.settings["yMin"]
        self.yMax = self.settings["yMax"]
        self.heightLine = self.yMax - self.yMin + settings["vMarginLineTop"]

        self.offsetLineMax = settings["offsetLineMax"]

        self.figs = []
        self.axs = []

        self._createCanvas(LocationFinder.getNumPages())

    def _createCanvas(self, numPages):

        for _ in range(numPages):
            fig, ax = plt.subplots(figsize=(self.settings["widthA4"], self.settings["heightA4"]))
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

