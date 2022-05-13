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
import json
import music21

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox
from matplotlib import rc



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

        self.LocationFinder = LocationFinder(self.streamObj, settings["offsetLineMax"])

        self.settings = self._computeSettings(settings)

        self.noteLowest, self.noteHighest = self._getRangeNotes()
        self.chords = len(self.streamObj.flat.getElementsByClass('Chord')) > 0
        self.yMin, self.yMax = self._getRangeYs()
        settings['yMin'], settings['yMax'] = self._getRangeYs()

        self.CanvasCreator = CanvasCreator(settings,
                                           self.LocationFinder.getNumLines(),
                                           self.LocationFinder.getLengthPickupMeasure(),
                                           self.yMin, self.yMax)

        key = self._getKey()
        self.PlotterNotes = PlotterNotes(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator, self.noteLowest,
                               key)
        self.PlotterChords = PlotterChords(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator, self.yMin,
                               key)
        self.PlotterBarlines = PlotterBarlines(self.streamObj, settings,
                               self.LocationFinder, self.CanvasCreator,
                               )
        self.PlotterMetadata = PlotterMetadata(self.streamObj, settings,
                               self.CanvasCreator.getAxs()[0], key)

    def generate(self, directoryName):
        self.plot()

        title = self.PlotterMetadata._getSongTitle()
        figs = self.CanvasCreator.getFigs()

        pathName = directoryName + f"{title}.pdf"

        with PdfPages(pathName) as pdf:
            for fig in figs:
                yPosLowest = self.CanvasCreator.getYPosLineBase(-1)
                yLengthAboveTitle = 1 - self.settings["yPosTitle"]
                if len(figs) == 1 and yPosLowest >= 0.55:
                    heightStart = self.settings["heightA4"] * (yPosLowest - yLengthAboveTitle)
                    bbox = Bbox([[0, heightStart], [self.settings["widthA4"], self.settings["heightA4"]]])
                    pdf.savefig(fig, bbox_inches=bbox)
                else:
                    pdf.savefig(fig)

        plt.close("all")

    def plot(self):

        # plt.rcParams.update({"text.usetex": False})
        self.PlotterMetadata.plotMetadata()
        rc('text.latex', preamble=r'\usepackage{amssymb}')
        # plt.rcParams.update({"text.usetex": True})
        self.PlotterNotes.plotNotes()
        self.PlotterChords.plotChords()
        self.PlotterBarlines.plotBarlines()

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

    def _getKey(self):
        if self.streamObj[music21.key.Key].first():
            key = self.streamObj[music21.key.Key].first()
        elif self.streamObj[music21.key.KeySignature].first():
            key1 = self.streamObj[music21.key.KeySignature].first().asKey()
            if self.settings["setInMajorKey"]:
                key = key1
            else:
                key = self.streamObj.analyze('key')
                if not (key == key1 or key == key1.relative):
                    print("analysed key does not correspond to keysignature")
        else:
            key = self.streamObj.analyze('key')
            print("no key signature found")

        if self.settings["setInMajorKey"] and key.mode == 'minor':
            key = key.relative

        return key


    def _computeSettings(self, settings):
        f = open('fontDimensions.json')
        fontDimensions = json.load(f)
        settings["capsizeNumberRelative"] = fontDimensions[settings["font"]]["capsize"]
        settings["widthNumberRelative"] = fontDimensions[settings["font"]]["width"]
        settings['capsizeNumberNote'] = fontDimensions[settings["font"]]["capsize"] * settings['fontSizeNotes']
        settings['widthNumberNote'] = fontDimensions[settings["font"]]["width"] * settings['fontSizeNotes']
        settings['fontSizeNoteAccidental'] = settings['fontSizeAccidentalRelative'] * settings['fontSizeNotes']
        settings['barSpace'] = settings['barSpacePerFontSize'] * settings['fontSizeNotes']
        settings['fontSizeChords'] = settings['fontSizeChordsPerFontSizeNotes'] * settings['fontSizeNotes']
        settings["xMinimalPickupMeasureSpace"] = settings["xMinimalPickupMeasureSpaceFraction"] * settings["offsetLineMax"]
        return settings


if __name__ == '__main__':

    path = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/standards_musescore/"
    song = "Alone_Together_Lead_sheet_with_lyrics_.mxl"
    song = "Misty.mxl"
    s = music21.converter.parse("/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/selection/Misty.mxl")
    # s = music21.converter.parse(path+song)
    # s = music21.converter.parse("/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/Use Me.mxl")

    # s = music21.converter.parse("/Users/jvo/Dropbox/Jesse/music/bladmuziek/standards_musescore/There_Will_Never_Be_Another_You.mxl")

    import json

    f = open('settings.json')

    settings = json.load(f)

    # settings["offsetLineMax"] = 8
    # settings["subdivision"] = 2
    # settings["setInMajorKey"] = False

    vis = Visualiser(s, settings)
    vis.generate("output/")

