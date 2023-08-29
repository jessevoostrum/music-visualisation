"""Jesse van Oostrum"""
import music21

from integerbook.plotter.PlotterMain import PlotterMain
from integerbook.LocationFinder import LocationFinder
from integerbook.CanvasCreator import CanvasCreator
from integerbook.Settings import Settings


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, pathToSong, userSettings=None):

        streamObj = music21.converter.parse(pathToSong)

        self.streamObj = self._preprocessStreamObj(streamObj)

        self.Settings = Settings(streamObj, userSettings)

        self.LocationFinder = LocationFinder(self.streamObj, self.Settings)

        yPosLowest = self.LocationFinder.getYPosLineBase(-1)
        self.CanvasCreator = CanvasCreator(self.Settings, self.LocationFinder.getNumPages(), yPosLowest)

        self.PlotterMain = PlotterMain(streamObj, self.Settings, self.LocationFinder, self.CanvasCreator.getAxs())

        self.PlotterMain.plot()

    def getSongTitle(self):
        return self.PlotterMain.PlotterMetadata.getSongTitle()

    def saveFig(self, dirName=None, buffer=None):
        if buffer:
            self.CanvasCreator.saveFig(buffer)
        else:
            title = self.getSongTitle()
            if not dirName:
                pathName = title + '.pdf'
            else:
                pathName = dirName + '/' + title + '.pdf'
            self.CanvasCreator.saveFig(pathName)

    def _preprocessStreamObj(self, streamObj):

        # streamObj = self._removeBassStaff(streamObj)
        streamObj = self._correctPickupMeasure(streamObj)

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

    def _correctPickupMeasure(self, streamObj):
        measures = streamObj[music21.stream.Measure]
        if measures[0].number == 1:
            if measures[0].quarterLength < measures[1].quarterLength:
                streamObj = self._renumberMeasures(streamObj)
        return streamObj

    def _renumberMeasures(self, streamObj):
        measures = streamObj[music21.stream.Measure]
        for i in range(len(measures)):
            measures[i].number = i
        return streamObj


if __name__ == '__main__':
    # import tracemalloc
    # pathToSong = "../../example/All_Of_Me.musicxml"
    #
    # tracemalloc.start()
    #
    # vis = Visualiser(pathToSong)
    #
    # vis.saveFig("/Users/jvo/Downloads/outputIBApp")
    #
    # print(tracemalloc.get_traced_memory())
    #
    # tracemalloc.stop()

    pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/Lullaby_of_Birdland_453af5e8-18cb-4b4c-9f0a-4baf7a27db8d.musicxml"
    pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/popular-sheets/All_Of_Me_de3dd464-e2bc-484a-837d-b9b77a7c28c9.musicxml"
    # pathToSong = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/documents/bladmuziek/test-files/notes-relative-to-chord.musicxml"
    pathToSong = "/Users/jvo/Downloads/output/notes-relative-to-chord.musicxml"
    # pathToSong = "/Users/jvo/Documents/programming/sheet-music/sheets/DSAll/Giant_Steps_d43d4d4c-7bf9-4c23-ade4-7352a541ccac.musicxml"

    vis = Visualiser(pathToSong)

    vis.saveFig("/Users/jvo/Downloads/output")