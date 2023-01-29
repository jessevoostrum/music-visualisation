import json
import os

import music21
import sample.aux.chordTypes as chordTypes
from sample.plotter.Plotter import Plotter

pathChordTypes = os.path.join(os.path.dirname(__file__), '../aux/chordTypes.json')
f = open(pathChordTypes)
chordTypes = json.load(f)


class PlotterChords(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):
        super().__init__(streamObj, settings, LocationFinder, axs)

        self.yMin = self.Settings.yMin

    def plotChords(self):
        chords = self.streamObj.flat.getElementsByClass('ChordSymbol')
        for i, chord, in enumerate(chords):
            offset = chord.offset

            if i > 0:
                offsetPreviousChord = chords[i-1].offset
                if offset == offsetPreviousChord:
                    continue

            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)

            xPos = xPos + self.Settings.xShiftChords
            yPos = self.yMin + yPosLineBase

            if chord.chordKind != 'none':    # not N.C.
                self._plotChordNumberAndAccidental(chord, xPos, yPos, page)

                self._plotAdditions(chord, xPos, yPos, page)

                self._plotBass(chord, xPos, yPos, page)

            else:
                self._plotNoChord(xPos, yPos, page)

    def _plotChordNumberAndAccidental(self, chordSymbol, xPos, yPos, page):
        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.Settings.getKey(offsetEl)
        number, accidental = key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())

        self.axs[page].text(xPos, yPos, number,
                            va='baseline', size=self.Settings.fontSizeChords)

        self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page)


    def _plotAdditions(self, chordSymbol, xPos, yPos, page):

        additions = self._findAdditions(chordSymbol)

        fontSize = self.Settings.fontSizeChords
        widthNumber = self.Settings.widthNumberRelative * fontSize

        xPos = xPos + widthNumber + self.Settings.hDistanceChordAddition
        yPos = yPos + self.Settings.capsizeNumberRelative * fontSize * 0.7

        self.fontSizeAddition = 10
        self.width = 0.01
        self.accidentalSpace = 0.01

        for i, addition in enumerate(additions):

            width = 0
            if addition == "minor":
                width = self._plotAdditionMinor(xPos, yPos, page)
            if addition == "major":
                width = self._plotAdditionMajor(xPos, yPos, page)
            if addition == 'half-diminished' :
                width = self._plotAdditionHalfDiminished(xPos, yPos, page)
            if addition == 'diminished':
                width = self._plotAdditionDiminished(xPos, yPos, page)


            if addition == "seventh":
                width = self._plotAdditionSeventh(xPos, yPos, page)
            if addition == "ninth":
                width = self._plotAdditionNinth(xPos, yPos, page)
            if addition == "11th":
                width = self._plotAddition11th(xPos, yPos, page)
            if addition == "13th":
                width = self._plotAddition13th(xPos, yPos, page)
            if addition == 'augmented':
                if i == 0:
                    xPos += 0.003
                else:
                    xPos += self.accidentalSpace
                width = self._plotAdditionAugmented(xPos, yPos, page)
            if addition == 'flat-five':
                width = self._plotAdditionFlatFive(xPos, yPos, page)

            xPos += width


    def _plotAdditionMinor(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "-", fontsize = self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width

    def _plotAdditionMajor(self, xPos, yPos, page):
        self.axs[page].text(xPos + 0.001, yPos - 0.0005,
                            "$\mathbb{\Delta}$", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width - 0.001

    def _plotAdditionHalfDiminished(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "o", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width

    def _plotAdditionDiminished(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "$\\varnothing$", fontsize=8,
                            va='baseline', ha='left', math_fontfamily='dejavusans')
        return self.width

    def _plotAdditionSeventh(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "7", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width

    def _plotAdditionNinth(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "9", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width

    def _plotAddition11th(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "11", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return 2 * self.width

    def _plotAddition13th(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "13", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return 2 * self.width


    def _plotAdditionAugmented(self, xPos, yPos, page):
        accidental = music21.pitch.Accidental('sharp')
        self._plotAccidental(accidental, self.fontSizeAddition, xPos, yPos, page)

        self.axs[page].text(xPos, yPos,
                            "5", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width

    def _plotAdditionFlatFive(self, xPos, yPos, page):
        accidental = music21.pitch.Accidental('flat')
        self._plotAccidental(accidental, self.fontSizeAddition, xPos, yPos, page)

        self.axs[page].text(xPos, yPos,
                            "5", fontsize=self.fontSizeAddition,
                            va='baseline', ha='left')
        return self.width


    def _findAdditions(self, chordSymbol):

        chordType = chordSymbol.chordKind

        # use the alias of the chord type that is used by music21
        if chordType in music21.harmony.CHORD_ALIASES:
            chordType = music21.harmony.CHORD_ALIASES[chordType]

        if chordType in chordTypes:
            additions = chordTypes[chordType]

        # for csMod in chordSymbol.chordStepModifications:
        #     if csMod.interval is not None:
        #         numAlter = csMod.interval.semitones
        #         if numAlter > 0:
        #             s = '\\#\!'
        #         else:
        #             s = 'b'
        #         prefix = s * abs(numAlter)
        #         if abs(numAlter) > 0:
        #             prefix = '\,{{}}^' + prefix
        #
        #         # print("numAlter", numAlter, "\n", "prefix", prefix)
        #
        #         # addition += ' ' + csMod.modType + ' ' + prefix + str(csMod.degree)
        #         addition += prefix + str(csMod.degree)
        #     else:
        #         # addition += ' ' + csMod.modType + ' ' + str(csMod.degree)
        #         addition += str(csMod.degree)

        return additions

    def _plotBass(self, chordSymbol, xPos, yPos, page):

        if chordSymbol.bass() is not None:
            if chordSymbol.root().name != chordSymbol.bass().name:

                fontSizeAddition = self.Settings.fontSizeAccidentalRelative * self.Settings.fontSizeChords

                key = self.Settings.getKey(chordSymbol.getOffsetInHierarchy(self.streamObj))

                pitch = chordSymbol.bass()
                number, accidental = key.getScaleDegreeAndAccidentalFromPitch(pitch)

                # plot slash
                xPosRightOfChord = xPos + 0.8 * self.Settings.widthNumberRelative * self.Settings.fontSizeChords
                yPosSlash = yPos - .4 * fontSizeAddition * self.Settings.capsizeNumberRelative

                self.axs[page].text(xPosRightOfChord, yPosSlash, '/', fontsize=fontSizeAddition,
                                    va='baseline', ha='left')

                # plot number
                xPosRightOfSlash = xPosRightOfChord + 0.8 * self.Settings.widthNumberRelative * fontSizeAddition
                xPosBass = xPosRightOfSlash
                if accidental:
                    xPosBass += 0.006

                yPosBass = yPosSlash - 0.25 * fontSizeAddition * self.Settings.capsizeNumberRelative

                self.axs[page].text(xPosBass, yPosBass, number, fontsize=fontSizeAddition,
                                    va='baseline', ha='left')

                # plot accidental
                self._plotAccidental(accidental, fontSizeAddition, xPosBass, yPosBass, page, addFontSize=0)


    def _plotNoChord(self, xPos, yPos, page):

        self.axs[page].text(xPos, yPos, 'N.C.',
                            va='baseline', size=self.Settings.fontSizeChords)

