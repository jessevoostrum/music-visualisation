import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

from integerbook.plotter.PlotterBase import Plotter



class PlotterMetadata(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):  #this class does actually not need LocationFinder

        super().__init__(streamObj, settings, LocationFinder, axs)

        self.ax = axs[0]

        self.offsetLineMax = self.Settings.offsetLineMax

        self.xPosLeft, self.xPosRight = self._computeXPos()


    def plotMetadata(self):
        self._plotTitle()
        self._plotComposer()
        self._plotArranger()
        self._plotKey()

    def _plotTitle(self):
        self.ax.text(0.5, self.Settings.yPosTitle,
                     self.getSongTitle(), fontsize=16, horizontalalignment='center',
                     verticalalignment='top')

    def _plotComposer(self):
        if self._getArranger() == "" or not self.Settings.printArranger:
            height = self.Settings.yPosArranger
        else:
            height = self.Settings.yPosComposer

        self.ax.text(self.xPosRight, height,
                          self._getComposer(), fontsize=self.Settings.fontSizeMetadata, horizontalalignment='right',
        verticalalignment='baseline')

    def _plotArranger(self):
        if self.Settings.printArranger:
            self.ax.text(self.xPosRight, self.Settings.yPosArranger,
                          self._getArranger(), fontsize=self.Settings.fontSizeMetadata, horizontalalignment='right',
                          verticalalignment='baseline')

    def _plotKey(self):

        key = self.Settings.getKey(0)
        number = "1"
        if self.Settings.numbersRelativeToChord:
            number = "I"
        self.ax.text(self.xPosLeft, self.Settings.yPosArranger,
                          f"{number} = {self._getKeyLetter(key)} ", fontsize=self.Settings.fontSizeMetadata, horizontalalignment='left',
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

    def _getArranger(self):
        player = ""
        try:
            contributors = self.streamObj.metadata.contributors
            for contributor in contributors:
                if contributor.role == 'arranger':
                    player = contributor.name
        except:
            pass
        return player


    def _computeXPos(self):
        offsetLengthLine = self.offsetLineMax + 2 * self.Settings.xMinimalPickupMeasureSpace
        plotSpace = 1 - 2 * self.Settings.widthMarginLine

        xPerOffset = plotSpace / offsetLengthLine

        xPosLeft = self.Settings.widthMarginLine + self.Settings.xMinimalPickupMeasureSpace * xPerOffset
        xPosRight = self.Settings.widthMarginLine + (self.Settings.xMinimalPickupMeasureSpace + self.Settings.offsetLineMax) * xPerOffset

        return xPosLeft, xPosRight