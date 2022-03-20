"""Jesse van Oostrum, November 12021
TODO:

- center number within 8th note or move it more to the left?
- for minor songs choice what is 1
- font title
- hammerOn pullOff
- work further on glissandos and other suggestions Jim
- multiple notes in chord
- repetition barLines and A, B, C part markers more clearly
- chord verbosity
- rewrite CanvasCreator so that it only creates a page and location management is all done in Plotter

rename
- Barline, facecolor, linewidth, etc.
- chordToneRatio


"""

import music21

from LocationFinder import LocationFinder
from CanvasCreator import CanvasCreator
from PlotterNotes import PlotterNotes
from PlotterChords import PlotterChords
from PlotterBarlines import PlotterBarlines
from PlotterMetadata import PlotterMetadata


class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, streamObj, settings):
        self.streamObj = streamObj

        self.LocationFinder = LocationFinder(self.streamObj, settings["xMax"])

        self.settings = self._computeSettings(settings)

        self.noteLowest, self.noteHighest = self._getRangeNotes()
        self.chords = len(self.streamObj.flat.getElementsByClass('Chord')) > 0
        self.yMin, self.yMax = self._getRangeYs()
        settings['yMin'], settings['yMax'] = self._getRangeYs()



        self.CanvasCreator = CanvasCreator(settings,
                                           self.LocationFinder.getNumLines(),
                                           self.LocationFinder.getLengthPickupMeasure(),
                                           self.yMin, self.yMax)

        key = self._getMajorKey()
        self.PlotterNotes = PlotterNotes(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator, self.noteLowest,
                               key)
        self.PlotterChords = PlotterChords(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator, self.yMin,
                               key)
        self.PlotterBarlines = PlotterBarlines(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator, self.yMin, self.yMax,
                               )
        self.PlotterMetadata = PlotterMetadata(self.streamObj, settings,
                               self.CanvasCreator.getTitleAx(), key)
    def plot(self):

        self.PlotterNotes.plotNotes()
        self.PlotterChords.plotChords()
        self.PlotterBarlines.plotBarlines()
        self.PlotterMetadata.plotMetadata()

    def _getRangeNotes(self):
        p = music21.analysis.discrete.Ambitus()
        pitchSpan = [int(thisPitch.ps) for thisPitch in p.getPitchSpan(self.streamObj)]
        return pitchSpan[0], pitchSpan[1]

    def _getRangeYs(self):
        numTones = self.noteHighest - self.noteLowest + 1
        yMax = numTones * self.settings["barSpace"] * (1 - self.settings["overlapFactor"]) + self.settings["barSpace"] * self.settings["overlapFactor"]
        if self.chords:
            yMin = - self.settings["chordToneRatio"] * self.settings["barSpace"]
        else:
            yMin = - self.settings["barSpace"] * .2  # why?
        return yMin, yMax

    def _getMajorKey(self):
        # no support for multiple keys
        # to recognise minor, one can use analyse method
        # key can be coded in mxl file as a key or keysignature
        if len(self.streamObj.flat.getElementsByClass(['KeySignature', 'Key'])) == 0:
            key = music21.key.Key('C')
        else:
            key = self.streamObj.flat.getElementsByClass('KeySignature')[0].asKey()
        return key

        # key = self.streamObj.analyze('key')
        # if key.mode == 'minor':
        #     key = key.relative
        # return key

    def _computeSettings(self, settings):
        settings['barSpace'] = settings['barSpacePerFontSize'] * settings['fontSizeNotes']
        settings['yShiftNumbers'] = settings['yShiftNumbersPerFontSize'] * settings['fontSizeNotes']
        settings['xWidthNumber'] = settings['xLengthNumberPerFontSize'] * settings['fontSizeNotes']
        settings['fontSizeChords'] = settings['fontSizeChordsPerFontSizeNotes'] * settings['fontSizeNotes']
        return settings





if __name__ == '__main__':

    s = music21.converter.parse("/Users/jvo/Dropbox/Jesse/music/bladmuziek/standards_musescore/All_Of_Me.mxl")

    s = music21.converter.parse("/Users/jvo/Dropbox/Jesse/music/bladmuziek/bass_lines_SBL/December 1963.mxl")

    s = music21.converter.parse("/Users/jvo/Dropbox/Jesse/music/bladmuziek/standards_musescore/There_Will_Never_Be_Another_You.mxl")

    import json

    f = open('settings.json')

    settings = json.load(f)

    # settings["xMax"] = 8
    # settings["subdivision"] = 2

    vis = Visualiser(s, settings)
    vis.plot()

    title = vis.PlotterMetadata._getSongTitle()

    figs = vis.CanvasCreator.getFigs()

    from matplotlib.backends.backend_pdf import PdfPages

    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    with PdfPages(f"output/{title}3.pdf") as pdf:
        for fig in figs:
            pdf.savefig(fig)

    import matplotlib.pyplot as plt
    plt.close("all")
