
from matplotlib import rc

from sample.plotter.PlotterNotes import PlotterNotes
from sample.plotter.PlotterChords import PlotterChords
from sample.plotter.PlotterBarlines import PlotterBarlines
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


    def plot(self):

        PN = PlotterNotes(self.streamObj, self.settings, self.LocationFinder, self.axs)
        PC = PlotterChords(self.streamObj, self.settings, self.LocationFinder, self.axs)
        PB = PlotterBarlines(self.streamObj, self.settings, self.LocationFinder, self.axs)
        PM = PlotterMetadata(self.streamObj, self.settings, self.LocationFinder, self.axs)
        #
        PM.plotMetadata()
        rc('text.latex', preamble=r'\usepackage{amssymb}')
        PN.plotNotes()
        PC.plotChords()
        PB.plotBarlines()