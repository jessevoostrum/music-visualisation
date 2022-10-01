"""Jesse van Oostrum"""
import json
import music21

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.transforms import Bbox

from sample.plotter.PlotterMain import PlotterMain
from LocationFinder import LocationFinder
from CanvasCreator import CanvasCreator



class Visualiser:
    """class for making visualisations from a music21 stream"""

    def __init__(self, streamObj, settings):
        self.streamObj = streamObj

        self.settings = settings
        self.settings = self._computeSettings(settings)

        self.LocationFinder = LocationFinder(self.streamObj, settings)

        self.CanvasCreator = CanvasCreator(settings, self.LocationFinder)

        self.PlotterMain = PlotterMain(streamObj, settings, self.LocationFinder, self.CanvasCreator.getAxs())

    def generate(self, directoryName):
        self.plot()

        # title = self.PlotterMetadata._getSongTitle() # TODO fix this
        title = "abc"
        figs = self.CanvasCreator.getFigs()

        pathName = directoryName + f"{title}.pdf"

        with PdfPages(pathName) as pdf:
            for fig in figs:
                yPosLowest = self.LocationFinder.getYPosLineBase(-1)
                yLengthAboveTitle = 1 - self.settings["yPosTitle"]
                if len(figs) == 1 and yPosLowest >= 0.55:
                    heightStart = self.settings["heightA4"] * (yPosLowest - yLengthAboveTitle)
                    bbox = Bbox([[0, heightStart], [self.settings["widthA4"], self.settings["heightA4"]]])
                    pdf.savefig(fig, bbox_inches=bbox)
                else:
                    pdf.savefig(fig)

        plt.close("all")

    def plot(self):

        self.PlotterMain.plot()



    def _computeSettings(self, settings):
        f = open('sample/fontDimensions.json')
        fontDimensions = json.load(f)
        settings["capsizeNumberRelative"] = fontDimensions[settings["font"]]["capsize"]
        settings["widthNumberRelative"] = fontDimensions[settings["font"]]["width"]
        settings['capsizeNumberNote'] = fontDimensions[settings["font"]]["capsize"] * settings['fontSizeNotes']
        settings['widthNumberNote'] = fontDimensions[settings["font"]]["width"] * settings['fontSizeNotes']
        settings['fontSizeNoteAccidental'] = settings['fontSizeAccidentalRelative'] * settings['fontSizeNotes']
        settings['barSpace'] = settings['barSpacePerFontSize'] * settings['fontSizeNotes']
        settings['fontSizeChords'] = settings['fontSizeChordsPerFontSizeNotes'] * settings['fontSizeNotes']
        settings['fontSizeGraceNotes'] = settings['fontSizeGraceNotesPerFontSizeNotes'] * settings['fontSizeNotes']
        settings["xMinimalPickupMeasureSpace"] = settings["xMinimalPickupMeasureSpaceFraction"] * settings["offsetLineMax"]
        settings["fontSizeSegno"] = settings["capsizeNumberRelative"] / fontDimensions["segno"] * settings['fontSizeNotes']
        settings["fontSizeCoda"] = settings["capsizeNumberRelative"] / fontDimensions["coda"] * settings['fontSizeNotes']
        settings["heightBarline0Extension"] = settings['capsizeNumberNote']
        settings["lengthFirstMeasure"] = self._getLengthFirstMeasure()
        settings["offsetLineMax"] = settings["lengthFirstMeasure"] * settings["measuresPerLine"]
        settings["noteLowest"], settings["noteHighest"] = self._getRangeNotes()
        settings['yMin'], settings['yMax'] = self._getRangeYs()
        settings['key'] = self._getKey()

        return settings

    def _getRangeNotes(self):
        p = music21.analysis.discrete.Ambitus()
        if p.getPitchSpan(self.streamObj):
            pitchSpan = [int(thisPitch.ps) for thisPitch in p.getPitchSpan(self.streamObj)]
            return pitchSpan[0], pitchSpan[1]
        else:
            return 1, 10

    def _getRangeYs(self):
        numTones = self.settings["noteHighest"] - self.settings["noteLowest"] + 1
        yMax = numTones * self.settings["barSpace"] * (1 - self.settings["overlapFactor"]) + self.settings["barSpace"] * self.settings["overlapFactor"]
        chords = len(self.streamObj.flat.getElementsByClass('Chord')) > 0
        if chords:
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
                try:
                    key = self.streamObj.analyze('key')
                except:
                    key = music21.key.Key('C')
                    print('key analysis failed')
                if not (key == key1 or key == key1.relative):
                    print("analysed key does not correspond to keysignature")
        else:
            try:
                key = self.streamObj.analyze('key')
            except:
                key = music21.key.Key('C')
                print('key analysis failed')
            print("no key signature found")

        if self.settings["setInMajorKey"] and key.mode == 'minor':
            key = key.relative

        return key


    def _getLengthFirstMeasure(self):
        length = self.streamObj.measure(1)[music21.stream.Measure][0].quarterLength
        return length


if __name__ == '__main__':

    pass
