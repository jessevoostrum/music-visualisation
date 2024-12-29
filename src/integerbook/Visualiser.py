"""Jesse van Oostrum"""
import music21

from integerbook.plotter.PlotterMain import PlotterMain
from integerbook.LocationFinder import LocationFinder
from integerbook.CanvasCreator import CanvasCreator
from integerbook.Settings import Settings
from integerbook.preprocessStreamObj import preprocessStreamObj


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, pathToSong, userSettings=None):

        streamObj = music21.converter.parse(pathToSong)

        self.streamObj = preprocessStreamObj(streamObj)

        self.Settings = Settings(self.streamObj, userSettings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        self.CanvasCreator = CanvasCreator(self.Settings, self.LocationFinder.getNumPages())

        self.PlotterMain = PlotterMain(self.streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

        self.PlotterMain.plot()

    def getSongTitle(self):
        return self.PlotterMain.PlotterMetadata.getSongTitle()

    def saveFig(self, dirName=None, buffer=None):
        yPosLowest = self.LocationFinder.getYPosLineBase(-1) + self.Settings.yMin
        if buffer:
            self.CanvasCreator.saveFig(buffer, yPosLowest)
        else:
            title = self.getSongTitle()
            if not dirName:
                pathName = title + '.pdf'
            else:
                pathName = dirName + '/' + title + '.pdf'
            self.CanvasCreator.saveFig(pathName, yPosLowest)



