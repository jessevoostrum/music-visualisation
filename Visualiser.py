import music21

from LocationFinder import LocationFinder
from CanvasCreator import CanvasCreator
from Plotter import Plotter


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, streamObj, measuresPerLine=4):
        self.streamObj = streamObj
        self.measuresPerLine = measuresPerLine

        self.LocationFinder = LocationFinder(self.streamObj, self.measuresPerLine)

        self.barSpace = 0.01  # relative to the height of an a4

        self.noteLowest, self.noteHighest = self.getRangeNotes()
        self.yMin, self.yMax = self.getRangeYs()

        self.CanvasCreator = CanvasCreator(self.LocationFinder.getNumLines(), self.yMin, self.yMax)

        self.Plotter = Plotter(self.streamObj, self.CanvasCreator.getAxs1D(), self.LocationFinder, self.barSpace,
                               self.noteLowest, self.yMin, self.yMax)

    def getRangeNotes(self):
        p = music21.analysis.discrete.Ambitus()
        pitchSpan = [int(thisPitch.ps) for thisPitch in p.getPitchSpan(self.streamObj)]
        return pitchSpan[0], pitchSpan[1]

    def getRangeYs(self):
        numTones = self.noteHighest - self.noteLowest + 1
        yMax = numTones * self.barSpace
        yMin = 0
        return yMin, yMax



if __name__ == '__main__':
    s = music21.converter.parse("tinyNotation: 4/4 c4 d e c c d e c e f g2 e4 f g2 "
                                "g8 a g f e4 c g8 a g f e4 c c4 G c2 c4 G c2"
                                )
    vis = Visualiser(s)
    vis.Plotter.plot()

