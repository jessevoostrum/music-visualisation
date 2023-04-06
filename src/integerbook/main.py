"""Jesse van Oostrum"""
import json
import os

import music21

from integerbook.plotter.PlotterMain import PlotterMain
from integerbook.LocationFinder import LocationFinder
from integerbook.CanvasCreator import CanvasCreator
from integerbook.Settings import Settings


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, pathToSong, settings=None):

        streamObj = music21.converter.parse(pathToSong)

        self.streamObj = self._preprocessStreamObj(streamObj)

        if not settings:
            pathSettings = os.path.join(os.path.dirname(__file__), 'settings.json')
            f = open(pathSettings)
            settings = json.load(f)

        self.Settings = Settings(streamObj, settings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        yPosLowest = self.LocationFinder.getYPosLineBase(-1)
        self.CanvasCreator = CanvasCreator(self.Settings, self.LocationFinder.getNumPages(), yPosLowest)

        self.PlotterMain = PlotterMain(streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

        self.PlotterMain.plot()

    def getSongTitle(self):
        return self.PlotterMain.PlotterMetadata.getSongTitle()

    def saveFig(self, dirName=None, buffer=None):
        if dirName:
            title = self.getSongTitle()
            pathName = dirName + '/' + title + '.pdf'
            self.CanvasCreator.saveFig(pathName)
        elif buffer:
            self.CanvasCreator.saveFig(buffer)

    def _preprocessStreamObj(self, streamObj):

        streamObj = self._removeBassStaff(streamObj)

        return streamObj

    def _removeBassStaff(self, streamObj):
        staffs = streamObj[music21.stream.PartStaff]
        if staffs:
            if len(staffs) > 1:
                streamObj.remove(staffs[1])
                print("removed staff")

        parts = streamObj[music21.stream.Part]
        if parts:
            if len (parts) > 1:
                streamObj.remove(parts[1:])
                print("removed part(s)")

        return streamObj


if __name__ == '__main__':
    pathToSong = "../../example/All_Of_Me.mxl"

    vis = Visualiser(pathToSong)

