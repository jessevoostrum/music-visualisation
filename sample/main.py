"""Jesse van Oostrum"""
import json
import music21

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox

from sample.plotter.PlotterMain import PlotterMain
from LocationFinder import LocationFinder
from CanvasCreator import CanvasCreator
from Settings import Settings




class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, streamObj, settings):
        self.streamObj = streamObj

        self.Settings = Settings(streamObj, settings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        self.CanvasCreator = CanvasCreator(self.Settings, self.LocationFinder)

        self.PlotterMain = PlotterMain(streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

    def generate(self, directoryName):
        self.plot()

        # title = self.PlotterMetadata._getSongTitle() # TODO fix this
        title = "abc"
        figs = self.CanvasCreator.getFigs()

        pathName = directoryName + f"{title}.pdf"

        with PdfPages(pathName) as pdf:
            for fig in figs:
                yPosLowest = self.LocationFinder.getYPosLineBase(-1)
                yLengthAboveTitle = 1 - self.Settings.yPosTitle
                if len(figs) == 1 and yPosLowest >= 0.55:
                    heightStart = self.Settings.heightA4 * (yPosLowest - yLengthAboveTitle)
                    bbox = Bbox([[0, heightStart], [self.Settings.widthA4, self.Settings.heightA4]])
                    pdf.savefig(fig, bbox_inches=bbox)
                else:
                    pdf.savefig(fig)

        plt.close("all")

    def plot(self):

        self.PlotterMain.plot()


if __name__ == '__main__':

    pass
