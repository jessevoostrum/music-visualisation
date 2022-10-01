import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

from sample.plotter.Plotter import Plotter



class PlotterMetadata(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):  #this class does actually not need LocationFinder

        super().__init__(streamObj, settings, LocationFinder, axs)

        self.ax = axs[0]

        self.offsetLineMax = settings["offsetLineMax"]

        self.key = settings["key"]

        self.xPosLeft, self.xPosRight = self._computeXPos()


    def plotMetadata(self):
        self._plotTitle()
        self._plotComposer()
        self._plotPlayer()
        self._plotKey()

    def _plotTitle(self):
        self.ax.text(0.5, self.settings["yPosTitle"],
                          self._getSongTitle(), fontsize=16, horizontalalignment='center',
        verticalalignment='top')

    def _plotComposer(self):
        if self._getPlayer() == "":
            height = self.settings["yPosPlayer"]
        else:
            height = self.settings["yPosComposer"]

        self.ax.text(self.xPosRight, height,
                          self._getComposer(), fontsize=self.settings["fontSizeMetadata"], horizontalalignment='right',
        verticalalignment='baseline')

    def _plotPlayer(self):
        self.ax.text(self.xPosRight, self.settings["yPosPlayer"],
                          self._getPlayer(), fontsize=self.settings["fontSizeMetadata"], horizontalalignment='right',
                          verticalalignment='baseline')

    def _plotKey(self):

        letter = self.key.tonic.name[0]

        self.ax.text(self.xPosLeft, self.settings["yPosPlayer"],
                          f"1 = {self._getKeyLetter()} ", fontsize=self.settings["fontSizeMetadata"], horizontalalignment='left',
                          verticalalignment='baseline')

    def _getSongTitle(self):
        try:
            songTitle = self.streamObj.metadata.title
        except:
            songTitle = "no title"
        return songTitle

    def _getComposer(self):
        try:
            composer = self.streamObj.metadata.composer
        except:
            composer = "no composer"
        return composer

    def _getPlayer(self):
        player = ""
        try:
            contributors = self.streamObj.metadata.contributors
            for contributor in contributors:
                if contributor.role == 'arranger':
                    player = contributor.name
        except:
            pass
        return player

    def _getKeyLetter(self):
        letter = self.key.tonic.name[0]
        accidental = self.key.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                letter = letter + "{}^\\#"
            elif accidental.name == 'flat':
                letter = letter + "{}^b"

        if self.key.mode == 'minor':
            letter += '-'

        letter = f"$\\mathregular{{{letter}}}$"

        return letter

    def _computeXPos(self):
        offsetLengthLine = self.offsetLineMax + 2 * self.settings["xMinimalPickupMeasureSpace"]
        plotSpace = 1 - 2 * self.settings["widthMarginLine"]

        xPerOffset = plotSpace / offsetLengthLine

        xPosLeft = self.settings["widthMarginLine"] + self.settings["xMinimalPickupMeasureSpace"] * xPerOffset
        xPosRight = self.settings["widthMarginLine"] + (self.settings["xMinimalPickupMeasureSpace"] + self.settings["offsetLineMax"]) * xPerOffset

        return xPosLeft, xPosRight