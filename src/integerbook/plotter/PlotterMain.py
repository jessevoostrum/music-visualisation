
from matplotlib import rc

from integerbook.plotter.PlotterNotes import PlotterNotes
from integerbook.plotter.PlotterChordsOld import PlotterChords
from integerbook.plotter.PlotterBarLines import PlotterBarLines
from integerbook.plotter.PlotterMetadata import PlotterMetadata

class Dog:
    def __int__(self, age):
        self.age = age

class PlotterMain:

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.Settings = Settings

        self.LocationFinder = LocationFinder

        self.axs = axs

        self.PlotterNotes = PlotterNotes(self.streamObj, self.Settings, self.LocationFinder, self.axs)
        self.PlotterChords = PlotterChords(self.streamObj, self.Settings, self.LocationFinder, self.axs)
        self.PlotterBarLines = PlotterBarLines(self.streamObj, self.Settings, self.LocationFinder, self.axs)
        self.PlotterMetadata = PlotterMetadata(self.streamObj, self.Settings, self.LocationFinder, self.axs)

    def plot(self):

        if self.Settings.plotMetadata:
            self.PlotterMetadata.plotMetadata()
        # rc('text.latex', preamble=r'\usepackage{amssymb}')

        if self.Settings.plotMelody:
            self.PlotterNotes.plotNotes()
        if self.Settings.plotChordNotes:
            self.PlotterNotes.plotChordNotes()

        if self.Settings.plotChords:
            self.PlotterChords.plotChords()

        if self.Settings.plotBarlines:
            self.PlotterBarLines.plotBarLines()

