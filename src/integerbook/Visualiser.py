"""Jesse van Oostrum"""
import music21

from integerbook.plotter.PlotterMain import PlotterMain
from integerbook.LocationFinder import LocationFinder
from integerbook.LocationFinderScroll import LocationFinderScroll
from integerbook.CanvasCreator import CanvasCreator
from integerbook.Settings import Settings
from integerbook.preprocessStreamObj import preprocessStreamObj


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, pathToSong, userSettings={}):

        self.Settings = Settings(userSettings)

        streamObj = music21.converter.parse(pathToSong)
        self.streamObj = preprocessStreamObj(streamObj, self.Settings)

        self.Settings.updateSettings(self.streamObj)

        if not self.Settings.scroll:
            self.LocationFinder = LocationFinder(self.streamObj, self.Settings)
        else:
            self.LocationFinder = LocationFinderScroll(self.streamObj, self.Settings)

        self.CanvasCreator = CanvasCreator(self.Settings,
                                           numPages=self.LocationFinder.getNumPages(),
                                           numMeasures=len(self.streamObj[music21.stream.Measure]) )

        self.PlotterMain = PlotterMain(self.streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

        self.PlotterMain.plot()

    def getSongTitle(self):
        return self.PlotterMain.PlotterMetadata.getSongTitle()

    def saveFig(self, dirName=None, buffer=None):
        yPosLowest = self.LocationFinder.getYPosLineBase(-1) + self.Settings.yMin
        maxXPos = self.LocationFinder.getMaxXPos()
        if buffer:
            self.CanvasCreator.saveFig(buffer, yPosLowest)
        else:
            title = self.getSongTitle()
            if not dirName:
                pathName = title
            else:
                pathName = dirName + '/' + title
            pathName += '.' + self.Settings.outputFormat

            self.CanvasCreator.saveFig(pathName, yPosLowest, self.LocationFinder.getMaxXPos())




