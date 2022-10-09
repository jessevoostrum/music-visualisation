"""Jesse van Oostrum"""




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
        self.PlotterMain.plot()

        title = self.PlotterMain.PlotterMetadata.getSongTitle()
        pathName = directoryName + f"{title}.pdf"
        yPosLowest = self.LocationFinder.getYPosLineBase(-1)

        self.CanvasCreator.saveFig(title, pathName, yPosLowest)


if __name__ == '__main__':

    pass
