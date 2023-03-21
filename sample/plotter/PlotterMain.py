
from matplotlib import rc

from sample.plotter.PlotterNotes import PlotterNotes
from sample.plotter.PlotterChords import PlotterChords
from sample.plotter.PlotterBarLines import PlotterBarLines
from sample.plotter.PlotterMetadata import PlotterMetadata

class Dog:
    def __int__(self, age):
        self.age = age

class PlotterMain:

    def __init__(self, streamObj, settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.settings = settings

        self.LocationFinder = LocationFinder

        self.axs = axs

        self.PlotterNotes = PlotterNotes(self.streamObj, self.settings, self.LocationFinder, self.axs)
        self.PlotterChords = PlotterChords(self.streamObj, self.settings, self.LocationFinder, self.axs)
        self.PlotterBarlines = PlotterBarLines(self.streamObj, self.settings, self.LocationFinder, self.axs)
        self.PlotterMetadata = PlotterMetadata(self.streamObj, self.settings, self.LocationFinder, self.axs)

    def plot(self):

        self.PlotterMetadata.plotMetadata()
        rc('text.latex', preamble=r'\usepackage{amssymb}')
        self.PlotterNotes.plotNotes()
        self.PlotterNotes.plotChordNotes()
        self.PlotterChords.plotChords()
        self.PlotterBarlines.plotBarLines()

