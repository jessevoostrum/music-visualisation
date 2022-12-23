import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

from sample.plotter.Plotter import Plotter



class PlotterMetadata(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):  #this class does actually not need LocationFinder

        super().__init__(streamObj, settings, LocationFinder, axs)

        self.ax = axs[0]

        self.offsetLineMax = self.Settings.offsetLineMax

        self.key = self.Settings.key

        self.xPosLeft, self.xPosRight = self._computeXPos()


    def plotMetadata(self):
        self._plotTitle()
        self._plotComposer()
        self._plotPlayer()
        self._plotKey()

    def _plotTitle(self):
        self.ax.text(0.5, self.Settings.yPosTitle,
                     self.getSongTitle(), fontsize=16, horizontalalignment='center',
                     verticalalignment='top')

    def _plotComposer(self):
        if self._getPlayer() == "":
            height = self.Settings.yPosPlayer
        else:
            height = self.Settings.yPosComposer

        self.ax.text(self.xPosRight, height,
                          self._getComposer(), fontsize=self.Settings.fontSizeMetadata, horizontalalignment='right',
        verticalalignment='baseline')

    def _plotPlayer(self):
        self.ax.text(self.xPosRight, self.Settings.yPosPlayer,
                          self._getPlayer(), fontsize=self.Settings.fontSizeMetadata, horizontalalignment='right',
                          verticalalignment='baseline')

    def _plotKey(self):

        letter = self.key.tonic.name[0]

        self.ax.text(self.xPosLeft, self.Settings.yPosPlayer,
                          f"1 = {self._getKeyLetter()} ", fontsize=self.Settings.fontSizeMetadata, horizontalalignment='left',
                          verticalalignment='baseline')

    def getSongTitle(self):
        try:
            songTitle = self.streamObj.metadata.bestTitle
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
        offsetLengthLine = self.offsetLineMax + 2 * self.Settings.xMinimalPickupMeasureSpace
        plotSpace = 1 - 2 * self.Settings.widthMarginLine

        xPerOffset = plotSpace / offsetLengthLine

        xPosLeft = self.Settings.widthMarginLine + self.Settings.xMinimalPickupMeasureSpace * xPerOffset
        xPosRight = self.Settings.widthMarginLine + (self.Settings.xMinimalPickupMeasureSpace + self.Settings.offsetLineMax) * xPerOffset

        return xPosLeft, xPosRight