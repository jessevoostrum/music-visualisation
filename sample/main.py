"""Jesse van Oostrum"""
import music21.stream

from sample.plotter.PlotterMain import PlotterMain
from sample.LocationFinder import LocationFinder
from sample.CanvasCreator import CanvasCreator
from sample.Settings import Settings


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, streamObj, settings):
        self.streamObj = self._preprocessStreamObj(streamObj)

        self.Settings = Settings(streamObj, settings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        self.CanvasCreator = CanvasCreator(self.Settings, self.LocationFinder.getNumPages())

        self.PlotterMain = PlotterMain(streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

    def generate(self, directoryName):
        self.PlotterMain.plot()

        title = self.PlotterMain.PlotterMetadata.getSongTitle()
        pathName = directoryName + f"{title}.pdf"
        yPosLowest = self.LocationFinder.getYPosLineBase(-1)

        self.CanvasCreator.saveFig(title, pathName, yPosLowest)

    def _preprocessStreamObj(self, streamObj):

        streamObj = self._removeBassStaff(streamObj)

        return streamObj

    def _removeBassStaff(self, streamObj):
        staffs = streamObj[music21.stream.PartStaff]
        if staffs:
            if len(staffs) > 1:
                streamObj.remove(staffs[1])
        return streamObj


if __name__ == '__main__':

    pass
