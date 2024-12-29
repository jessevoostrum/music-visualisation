"""Jesse van Oostrum"""
import music21

from integerbook.plotter.PlotterMain import PlotterMain
from integerbook.LocationFinderScroll import LocationFinder
from integerbook.CanvasCreatorScroll import CanvasCreator
from integerbook.Settings import Settings
from integerbook.preprocessStreamObj import preprocessStreamObj

class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, pathToSong, userSettings=None):

        streamObj = music21.converter.parse(pathToSong)
        numMeasures = len(streamObj[music21.stream.Measure])

        self.streamObj = preprocessStreamObj(streamObj)

        self.Settings = Settings(self.streamObj, userSettings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        self.CanvasCreator = CanvasCreator(self.Settings, numMeasures)

        self.PlotterMain = PlotterMain(self.streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

        self.PlotterMain.plot()

    def getSongTitle(self):
        return self.PlotterMain.PlotterMetadata.getSongTitle()

    def saveFig(self, dirName=None):
        title = self.getSongTitle()
        if not dirName:
            pathName = title
        else:
            pathName = dirName + '/' + title
        pathName += '.' + self.Settings.outputFormat

        self.CanvasCreator.saveFig(pathName, self.LocationFinder.getMaxXPos())



