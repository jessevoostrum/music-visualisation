import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


class PlotterMetadata:

    def __init__(self, streamObj, settings, ax, key):

        self.streamObj = streamObj
        self.settings = settings

        self.ax = ax

        self.offsetLineMax = settings["offsetLineMax"]

        self.key = key

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
                          self._getComposer(), fontsize=10, horizontalalignment='right',
        verticalalignment='center')

    def _plotPlayer(self):
        self.ax.text(self.xPosRight, self.settings["yPosPlayer"],
                          self._getPlayer(), fontsize=10, horizontalalignment='right',
                          verticalalignment='center')

    def _plotKey(self):

        self.ax.text(self.xPosLeft, self.settings["yPosPlayer"],
                          f"1 = {self._getKeyLetter()} ", fontsize=10, horizontalalignment='left',
                          verticalalignment='center')

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
        # letter = f"\mathrm{{{self.key.tonic.name[0]}}}"
        letter = self.key.tonic.name[0]
        accidental = self.key.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                # letter = f"{letter}^\\#"
                letter = letter + "${}^\\#$"
            elif accidental.name == 'flat':
                # letter = f"{letter}^b"
                letter = letter + "${}^b$"


        return letter

    def _computeXPos(self):
        offsetLengthLine = self.offsetLineMax + 2 * self.settings["xMinimalPickupMeasureSpace"]
        plotSpace = 1 - 2 * self.settings["widthMarginLine"]

        xPerOffset = plotSpace / offsetLengthLine

        xPosLeft = self.settings["widthMarginLine"] + self.settings["xMinimalPickupMeasureSpace"] * xPerOffset
        xPosRight = self.settings["widthMarginLine"] + (self.settings["xMinimalPickupMeasureSpace"] + self.settings["offsetLineMax"]) * xPerOffset

        return xPosLeft, xPosRight