import music21
from matplotlib.patches import Polygon
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np


class PlotterMetadata:

    def __init__(self, streamObj, settings, titleAx, key):

        self.streamObj = streamObj
        self.settings = settings

        self.titleAx = titleAx

        self.xMax = settings["xMax"]

        self.key = key


    def plotMetadata(self):
        self._plotTitle()
        self._plotComposer()
        self._plotPlayer()
        self._plotKey()

    def _plotTitle(self):
        self.titleAx.text(self.xMax / 2, self.settings["heightTitle"],
                          self._getSongTitle(), fontsize=16, horizontalalignment='center',
        verticalalignment='top')

    def _plotComposer(self):
        if self._getPlayer() == "":
            height = self.settings["heightPlayer"]
        else:
            height = self.settings["heightComposer"]

        self.titleAx.text(self.xMax, height,
                          self._getComposer(), fontsize=10, horizontalalignment='right',
        verticalalignment='center')

    def _plotPlayer(self):
        self.titleAx.text(self.xMax, self.settings["heightPlayer"],
                          self._getPlayer(), fontsize=10, horizontalalignment='right',
                          verticalalignment='center')

    def _plotKey(self):

        self.titleAx.text(0, self.settings["heightPlayer"],
                          f"$1 = {self._getKeyLetter()} $", fontsize=10, horizontalalignment='left',
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
        letter = f"\mathrm{{{self.key.tonic.name[0]}}}"
        accidental = self.key.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                letter = f"{letter}^\\#"
            elif accidental.name == 'flat':
                letter = f"{letter}^b"

        return letter
