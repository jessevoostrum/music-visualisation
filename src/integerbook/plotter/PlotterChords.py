import math
import json
import os

import music21

from integerbook.plotter.PlotterBase import Plotter
from matplotlib.patches import Ellipse, Polygon

from integerbook.plotter.patches import Triangle, Doughnut, Slash


class PlotterChords(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):
        super().__init__(streamObj, settings, LocationFinder, axs)

        self.yMin = self.Settings.yMin


        pathChordKindAbbreviations = os.path.join(os.path.dirname(__file__), 'chordKindAbbreviations.json')
        f = open(pathChordKindAbbreviations)
        self.chordKindAbbreviations = json.load(f)



    def plotChords(self):
        chordSymbols = self.streamObj[music21.harmony.ChordSymbol]
        for idxChord, chordSymbol, in enumerate(chordSymbols):

            offset = chordSymbol.getOffsetInHierarchy(self.streamObj)
            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)
            key = self.getKey(offset)

            xPos = xPos + self.Settings.xShiftChords
            yPos = self.yMin + yPosLineBase

            plottedNumeral = self._plotRomanNumeral(chordSymbol, key, xPos, yPos, page)

            xPos += self._getPlottedWidth(plottedNumeral, page)

            self._plotKindAndModifcations(chordSymbol, xPos, yPos, page, self.Settings.fontSizeType, self.Settings.capsizeChord)

            self._plotBass(chordSymbol, key, xPos, yPos, page)

        self._plotSecondaryChords()

    def _plotRomanNumeral(self, chordSymbol, key, xPos, yPos, page):
        number, accidental = self.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root(), key)
        numeral = self._intToRoman(number)
        if self._isMinor(chordSymbol):
            numeral = numeral.lower()
        if accidental:
            numeral = accidental.unicode + numeral

        return self.axs[page].text(xPos, yPos, numeral, va='baseline', size=self.Settings.fontSizeChords,
                            color=self.Settings.colorTextChords)



    def _plotKindAndModifcations(self, chordSymbol, xPos, yPos, page, fontSizeType, capsizeChord):
        chordKind = self.chordKindAbbreviations[chordSymbol.chordKind]
        modifications = self._getModifications(chordSymbol)

        yPosKindAndModification = yPos + 0.6 * capsizeChord

        return self.axs[page].text(xPos, yPosKindAndModification, chordKind + modifications, va='baseline', size=fontSizeType,
                                   color=self.Settings.colorTextChords)


    def _plotBass(self, chordSymbol, key, xPos, yPos, page):

        if chordSymbol.root().name != chordSymbol.bass().name:

            key = self.getKey(chordSymbol.getOffsetInHierarchy(self.streamObj))

            pitch = chordSymbol.bass()
            number, accidental = self.getScaleDegreeAndAccidentalFromPitch(pitch, key, accidentalAsString=True)

            text = '/' + accidental + str(number)

            yPosBass = yPos - 0.5 * self.Settings.capsizeChord

            self.axs[page].text(xPos, yPosBass, text, fontsize=self.Settings.fontSizeType,
                                va='baseline', ha='left', color=self.Settings.colorTextChords)

    def _plotSecondaryChords(self):
        for chordInfo in self.Settings.manualSecondaryChords:
            measureNumber, chordIndexWithinMeasure = chordInfo[0]
            numeralFunction, numeralKey = [self._formatManualNumeral(chordInfo[i]) for i in [1,2]]

            try:
                chordSymbol = self.streamObj.measure(measureNumber)[music21.harmony.ChordSymbol][chordIndexWithinMeasure]
            except IndexError:
                print("Index secondary chord out of range")

            offset = chordSymbol.getOffsetInHierarchy(self.streamObj)
            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)
            key = self.getKey(offset)

            xPos = xPos + self.Settings.xShiftChords
            yPos = self.yMin + yPosLineBase - 2 * self.Settings.capsizeSecondaryChord

            plottedNumeral = self.axs[page].text(xPos, yPos, numeralFunction, va='baseline', size=self.Settings.fontSizeSecondaryChord,
                                                 color=self.Settings.colorTextChords)

            xPos += self._getPlottedWidth(plottedNumeral, page)

            plottedKindAndModification = self._plotKindAndModifcations(chordSymbol, xPos, yPos, page,
                                                                       self.Settings.fontSizeTypeSecondaryChord,
                                                                       self.Settings.capsizeSecondaryChord)

            xPos += self._getPlottedWidth(plottedKindAndModification, page)

            plottedNumeral = self.axs[page].text(xPos, yPos, '/' + numeralFunction, va='baseline',
                                                 size=self.Settings.fontSizeSecondaryChord,
                                                 color=self.Settings.colorTextChords)


    def _formatManualNumeral(self, manualNumeral):
        return manualNumeral.replace("#", "♯").replace("b", "♭")

    def _getModifications(self, chordSymbol):

        modificationsString = ""

        for csMod in chordSymbol.chordStepModifications:
            modificationsString += self._getModType(csMod, chordSymbol.chordKind)
            modificationsString += self._intervalToAccidentalString(csMod.interval)
            modificationsString += str(csMod.degree)

        return modificationsString


    def _getModType(self, csMod, chordKind):
        d = {
            "add": "add",
            "subtract": "omit",
            "alter": ""
        }
        modType = d[csMod.modType]
        if self._isAddAndNotTriadAndAccidentalModification(csMod, chordKind):
            modType = ""

        return modType

    def _isAddAndNotTriadAndAccidentalModification(self, csMod, chordKind):
        "e.g. C7♭9. We check this to avoid having expressions like c7add♭9  "
        return csMod.modType == "add" and not self._isTriad(chordKind) and not csMod.interval.semitones == 0

    def _isTriad(self, chordKind):
        triadTypes = {"major", "minor", "augmented", "diminished", "suspended-second", "suspended-fourth"}
        return chordKind in triadTypes

    def _getScaleDegreesFromChordKind(self, chordKind):
        return music21.harmony.CHORD_TYPES[chordKind][0].split(',')

    def _intervalToAccidentalString(self, interval):
        if interval.semitones == 0:
            return ""
        else:
            return music21.pitch.Accidental(interval.semitones).unicode

    def _intToRoman(self, number):
        roman_mapping = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V",
            6: "VI",
            7: "VII"
        }
        return roman_mapping.get(number, "Invalid input")

    def _isMinor(self, chordSymbol):
        return '-3' in self._getScaleDegreesFromChordKind(chordSymbol.chordKind)

    def _getPlottedWidth(self, plottedObject, page):
        renderer = self.axs[page].figure._get_renderer()
        bb = plottedObject.get_window_extent(renderer=renderer).transformed(self.axs[page].transData.inverted())
        return bb.width



        # if chord.chordKind != 'none':    # not N.C.
            #     if not self.Settings.romanNumerals:
            #         widthNumber = self._plotChordNumberAndAccidental(chord, xPos, yPos, page)
            #
            #         self._plotTypesAndModifications(chord, xPos, yPos, page, widthNumber)
            #
            #         self._plotBass(chord, xPos, yPos, page)
            #
            #     else:
            #         widthNumber = self._plotRomanNumeralAndAccidental(chord, xPos, yPos, page, idxChord, chords)
            #
            #         xPos = self._plotTypesAndModifications(chord, xPos, yPos, page, widthNumber)
            #
            #         self._plotSecondaryTargetNumeral(chord, xPos, yPos, page, idxChord)
            #
            #         # self._plotBass(chord, xPos, yPos, page)
            #
            # else:
            #     self._plotNoChord(xPos, yPos, page)

    def _plotChordNumberAndAccidental(self, chordSymbol, xPos, yPos, page):
        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.getKey(offsetEl)
        number, accidental = self.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root(), key)

        chordNumber = number

        self.text = self.axs[page].text(xPos, yPos, chordNumber, va='baseline', size=self.Settings.fontSizeChords,
                                        color=self.Settings.colorTextChords)
        plottedNumber = self.text

        widthNumber = self._getPlottedWidth(page, plottedNumber)

        self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page,
                             colorText=self.Settings.colorTextChords)

        return widthNumber

    def _plotTypesAndModifications(self, chordSymbol, xPos, yPos, page, widthNumber):

        if not self.Settings.romanNumerals:
            widthNumber = self.Settings.fontWidthChord

        xPos = xPos + widthNumber + self.Settings.fontSettings.hDistanceChordAddition
        yPos = yPos + self.Settings.capsizeChord * self.Settings.heightChordAddition

        self.fontSizeType = self.Settings.fontSizeType
        self.fontSizeTypeSmall = self.Settings.fontSizeTypeSmall
        self.width = self.Settings.fontSettings.widthCharacter
        self.accidentalSpace = self.Settings.fontSettings.accidentalSpace

        xPos = self._plotTypes(chordSymbol, xPos, yPos, page)

        xPos = self._plotModifications(chordSymbol, xPos, yPos, page)

        return xPos

    def _plotTypes(self, chordSymbol, xPos, yPos, page):
        chordTypes = self._getTypeList(chordSymbol)

        for i, chordType in enumerate(chordTypes):

            if self.Settings.romanNumerals:
                if chordType == "minor":
                    continue

            width = 0
            if chordType == "minor":
                width = self._plotTypeMinor(xPos, yPos, page)

            if self.Settings.chordVerbosity > 0:

                if chordType == "major" and len(chordTypes) != 1 and chordTypes[i+1] != 'sixth':
                    width = self._plotTypeMajor(xPos, yPos, page)
                if chordType == 'half-diminished':
                    width = self._plotTypeDiminishedOrHalfDiminished(xPos, yPos, page, halfDiminished=True)
                if chordType == 'diminished':
                    width = self._plotTypeDiminishedOrHalfDiminished(xPos, yPos, page, halfDiminished=False)

                if chordType == "sixth":
                    width = self._plotTypeSixth(xPos, yPos, page)
                if chordType == "seventh":
                    width = self._plotTypeSeventh(xPos, yPos, page)
                if chordType == "ninth":
                    width = self._plotTypeNinth(xPos, yPos, page)
                if chordType == "11th":
                    width = self._plotType11th(xPos, yPos, page)
                if chordType == "13th":
                    width = self._plotType13th(xPos, yPos, page)

                if chordType == 'augmented':
                    if i == 0:
                        xPos -= 0.7 * self.Settings.fontSettings.accidentalSpace
                    width = self._plotTypeAugmented(xPos, yPos, page)
                if chordType == 'suspended-second':
                    width = self._plotTypeSuspendedSecond(xPos, yPos, page)
                if chordType == 'suspended-fourth':
                    width = self._plotTypeSuspendedFourth(xPos, yPos, page)
            xPos += width
        return xPos

    def _plotModifications(self, chordSymbol, xPos, yPos, page):

        noTypesPrinted = self._noTypesPrinted(chordSymbol)

        if self.Settings.chordVerbosity > 0:
            firstAdd = True
            for i, csMod in enumerate(chordSymbol.chordStepModifications):
                if csMod.interval is not None:
                    width = 0
                    if csMod.modType == 'add':
                        if self.Settings.chordVerbosity == 1:
                            continue
                        if not firstAdd:
                            width = self._plotComma(xPos, yPos, page)
                        if noTypesPrinted and firstAdd:
                            width = self._plotModificationAdd(xPos, yPos, page)
                            firstAdd = False
                    if csMod.modType == 'subtract':
                        if self.Settings.chordVerbosity == 1:
                            continue
                        width = self._plotModificationSubtract(xPos, yPos, page)
                    if csMod.modType == 'alter':
                        if noTypesPrinted:
                            xPos -= 0.7 * self.accidentalSpace
                        # width = self._plotModificationAlter(xPos, yPos, page)

                    xPos += width

                    number = csMod.degree

                    accidental = None
                    if csMod.interval.semitones == -1:
                        accidental = music21.pitch.Accidental('flat')
                    if csMod.interval.semitones == 1:
                        accidental = music21.pitch.Accidental('sharp')

                    width = self._plotTypeAndModificationNumberAndAccidental(number, accidental, xPos, yPos, page)

                    xPos += width
            return xPos

    def _plotTypeAndModificationNumberAndAccidental(self, number, accidental, xPos, yPos, page):

        if self.Settings.fontVShift:  # this is for fonts that are not placed exactly on the baseline (vertically)
            yPos += self.Settings.fontVShift * self.Settings.capsizeNumberRelative * self.fontSizeType

        width = 0
        if accidental:
            xPos += self.accidentalSpace
            width += self.accidentalSpace

        self._plotAccidental(accidental, self.fontSizeType, xPos, yPos, page, colorText=self.Settings.colorTextChords)

        self.axs[page].text(xPos, yPos,
                            f"{number}", fontsize=self.fontSizeType,
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        width += len(str(number)) * self.width

        return width

    def _plotTypeMinor(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos + 0.00005 * self.fontSizeType,
                            u'\u2013', fontsize=self.fontSizeType,
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self.Settings.fontSettings.widthMinus

    def _plotTypeMajor(self, xPos, yPos, page):
        xShift = 0.0002 * self.fontSizeType
        spaceAfter = 0.000082 * self.fontSizeType
        height = self.Settings.capsizeType * .9
        width = 0.00095 * self.fontSizeType

        xPos += xShift

        patch = Triangle(xPos, yPos, height, width, self.Settings.xyRatio, colorText=self.Settings.colorTextChords)

        self.axs[page].add_patch(patch)

        return xShift + width + spaceAfter



    def _plotTypeDiminishedOrHalfDiminished(self, xPos, yPos, page, halfDiminished=False):

        xShift = 0.0001 * self.fontSizeType
        spaceAfter = 0.00012 * self.fontSizeType

        xPos += xShift
        height = self.Settings.capsizeType * 0.73


        xyRatio = self.Settings.widthA4 / self.Settings.heightA4
        diameterX = height / xyRatio

        patch = Doughnut(xPos, yPos, height, xyRatio, colorText=self.Settings.colorTextChords)

        self.axs[page].add_patch(patch)

        if halfDiminished:
            patch = Slash(xPos, yPos, height, xyRatio, colorText=self.Settings.colorTextChords)
            self.axs[page].add_patch(patch)

        return diameterX + xShift + spaceAfter

    def _plotTypeSixth(self, xPos, yPos, page):
        width = self._plotTypeAndModificationNumberAndAccidental(6, None, xPos, yPos, page)
        return width

    def _plotTypeSeventh(self, xPos, yPos, page):
        width = self._plotTypeAndModificationNumberAndAccidental(7, None, xPos, yPos, page)
        return width

    def _plotTypeNinth(self, xPos, yPos, page):
        width = self._plotTypeAndModificationNumberAndAccidental(9, None, xPos, yPos, page)
        return width

    def _plotType11th(self, xPos, yPos, page):
        width = self._plotTypeAndModificationNumberAndAccidental(11, None, xPos, yPos, page)
        return width

    def _plotType13th(self, xPos, yPos, page):
        width = self._plotTypeAndModificationNumberAndAccidental(13, None, xPos, yPos, page)
        return width

    def _plotTypeAugmented(self, xPos, yPos, page):
        xPos += self.accidentalSpace
        accidental = music21.pitch.Accidental('sharp')
        self._plotAccidental(accidental, self.fontSizeType, xPos, yPos, page, colorText=self.Settings.colorTextChords)

        self.axs[page].text(xPos, yPos,
                            "5", fontsize=self.fontSizeType,
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self.width + self.accidentalSpace

    def _plotTypeSuspendedSecond(self, xPos, yPos, page):

        widthSus = self._plotSus(xPos, yPos, page)

        xPos2 = xPos + widthSus

        self.axs[page].text(xPos2, yPos,
                            "2", fontsize=self.fontSizeType, # fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)

        return self.width + widthSus

    def _plotTypeSuspendedFourth(self, xPos, yPos, page):
        widthSus = self._plotSus(xPos, yPos, page)

        xPos4 = xPos + widthSus

        self.axs[page].text(xPos4, yPos,
                            "4", fontsize=self.fontSizeType,
                            va='baseline', ha='left', color=self.Settings.colorTextChords)

        return self.width + widthSus

    def _plotSus(self, xPos, yPos, page):
        plottedObject = self.axs[page].text(xPos, yPos,
                            "sus", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)

        return self._getPlottedWidth(page, plottedObject) + self.Settings.fontSettings.spaceAfterAddSus

    def _plotModificationAdd(self, xPos, yPos, page):
        plottedObject = self.axs[page].text(xPos, yPos,
                            "add", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self._getPlottedWidth(page, plottedObject) + self.Settings.fontSettings.spaceAfterAddSus

    def _plotModificationSubtract(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "sub", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self.Settings.fontSettings.spaceAddSus

    def _plotModificationAlter(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "alt", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self.Settings.fontSettings.spaceAddSus

    def _plotComma(self, xPos, yPos, page):
        plottedObject = self.axs[page].text(xPos, yPos,
                            ",", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left', color=self.Settings.colorTextChords)
        return self._getPlottedWidth(page, plottedObject)

    @staticmethod
    def _getTypeList(chordSymbol):
        # see: https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/kind-value/
        chordType = chordSymbol.chordKind

        # use the alias of the chord type that is used by music21
        if chordType in music21.harmony.CHORD_ALIASES:
            chordType = music21.harmony.CHORD_ALIASES[chordType]

        types = []
        if 'minor' in chordType:
            types.append("minor")
        if 'major' in chordType:
            types.append("major")
        if 'half-diminished' in chordType:
            types.append("half-diminished")
        if 'diminished' in chordType and not 'half-diminished' in chordType:
            types.append("diminished")

        if 'seventh' in chordType:
            types.append("seventh")
        if 'sixth' in chordType:
            types.append("sixth")
        if 'ninth' in chordType:
            types.append("ninth")
        if '11th' in chordType:
            types.append("11th")
        if '13th' in chordType:
            types.append("13th")

        if 'augmented' in chordType:
            types.append("augmented")

        if 'suspended-second' in chordType:
            types.append("suspended-second")
        if 'suspended-fourth' in chordType:
            types.append("suspended-fourth")

        if 'Neapolitan' in chordType:
            types.append("Neapolitan")
        if 'Italian' in chordType:
            types.append("Italian")
        if 'French' in chordType:
            types.append("French")
        if 'German' in chordType:
            types.append("German")
        if 'pedal' in chordType:
            types.append("pedal")
        if 'power' in chordType:
            types.append("power")
        if 'Tristan' in chordType:
            types.append("Tristan")

        return types


    def _plotNoChord(self, xPos, yPos, page):

        self.axs[page].text(xPos, yPos, 'N.C.',
                            va='baseline', size=self.Settings.fontSizeChords, color=self.Settings.colorTextChords)

    def _plotRomanNumeralAndAccidental(self, chordSymbol, xPos, yPos, page, idxChord, chords):

        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.getKey(offsetEl)
        number, accidental = self.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root(), key)

        chordNumber = self._getRomanNumeral(number, key, chordSymbol)
        if str(idxChord) in self.manualRomanNumeralDict.keys():
            chordNumber = self.manualRomanNumeralDict[str(idxChord)]['numeral']
            accidental = self.manualRomanNumeralDict[str(idxChord)]['accidental']

        elif self._plotAsSecondaryDominant(chordSymbol, key, idxChord):
            chordNumber = self._rootSecondaryChord(idxChord)
            accidental = self._accidentalRootSecondaryChord(idxChord)

        plottedNumber = self.axs[page].text(xPos, yPos, chordNumber,
                                            va='baseline', size=self.Settings.fontSizeChords, color=self.Settings.colorTextChords)

        widthNumber = self._getPlottedWidth(page, plottedNumber)

        self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page, colorText=self.Settings.colorTextChords)

        return widthNumber

    def _getPlottedWidth(self, plottedObject, page):
        renderer = self.axs[page].figure._get_renderer()
        bb = plottedObject.get_window_extent(renderer=renderer).transformed(self.axs[page].transData.inverted())
        return bb.width

    def _plotSecondaryTargetNumeral(self, chordSymbol, xPos, yPos, page, idxChord):
        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.getKey(offsetEl)
        if self._plotAsSecondaryDominant(chordSymbol, key, idxChord):
            target = self._targetSecondaryChord(chordSymbol, key, idxChord)
            accidental = self._accidentalTargetSecondaryChord(idxChord)
            plottedSlash = self.axs[page].text(xPos, yPos, "\\",
                                                    va='baseline', size=self.Settings.fontSizeChords, color=self.Settings.colorTextChords)
            widthSlash = self._getPlottedWidth(page, plottedSlash)
            xPos += widthSlash
            if accidental:
                xPos += self.Settings.fontWidthChord * 0.1
            self.axs[page].text(xPos, yPos, target,
                                va='baseline', size=self.Settings.fontSizeChords, color=self.Settings.colorTextChords)
            self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page)

    def _plotAsSecondaryDominant(self, chordSymbol, key, idxChord):
        if str(idxChord) in self.manualSecondaryChordDict.keys():
            return True
        elif self.Settings.onlyManualSecondaryDominants:
            return False
        elif idxChord in self.ignoreSecondaryDominants or str(idxChord) in self.manualRomanNumeralDict.keys():
            return False
        elif self._isSecondaryDominant(chordSymbol, key):
            return True
        return False

    def _rootSecondaryChord(self, idxChord):
        if str(idxChord) in self.manualSecondaryChordDict.keys():
            return self.manualSecondaryChordDict[str(idxChord)]["root"]
        else:
            return "V"

    def _targetSecondaryChord(self, chordSymbol, key, idxChord):
        if str(idxChord) in self.manualSecondaryChordDict.keys():
            return self.manualSecondaryChordDict[str(idxChord)]["target"]
        else:
            return self._targetSecondaryDominant(chordSymbol, key)

    def _accidentalRootSecondaryChord(self, idxChord):
        if str(idxChord) in self.manualSecondaryChordDict.keys():
            accidental = self.manualSecondaryChordDict[str(idxChord)]['accidentalRoot']
            if accidental:
                music21.pitch.Accidental(accidental)
        return None

    def _accidentalTargetSecondaryChord(self, idxChord):
        if str(idxChord) in self.manualSecondaryChordDict.keys():
            accidental = self.manualSecondaryChordDict[str(idxChord)]['accidentalTarget']
            if accidental:
                return music21.pitch.Accidental(accidental)
        return None


    def _isSecondaryDominant(self, chordSymbol, key):
        if self._isMajor(chordSymbol) and (self._isTriad(chordSymbol) or self._hasDominantSeventh(chordSymbol)) and \
                self._rootEqualsBass(chordSymbol):
            number, accidental = self.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root(), key)
            if not accidental:
                if key.mode == 'major':
                    if number == 1:
                        if self._hasDominantSeventh(chordSymbol):
                            return True
                    if number in [6, 7, 2, 3]:   # see Mulholland page 40. this corresponds to V/ii, V/iii, etc.
                        return True
                if key.mode == 'minor':
                    if number == 3:
                        if self._hasDominantSeventh(chordSymbol):
                            return True
                    if number in [2, 1, 7]:  # less common secondary dominants (see Mulholland p101) are not implemented
                        return True
        return False

    def _targetSecondaryDominant(self, chordSymbol, key):
        number, accidental = self.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root(), key)
        targetNumber = (number + 3) % 7
        return self._getRomanNumeral(targetNumber, key)

    def _convertMeasureChordIdcsToGlobalIdcs(self, measureChordIdcs):
        globalChordIdcs = []
        for measureChordIdx in measureChordIdcs:
            globalChordIdx = self._measureChordIdxToGlobalChordIdx(measureChordIdx)
            globalChordIdcs.append(globalChordIdx)
        return globalChordIdcs

    def _makeManualSecondaryChordDict(self, manualSecondaryChords):
        manualSecondaryChordDict = {}
        for manualSecondaryChord in manualSecondaryChords:
            globalChordlIdx = self._measureChordIdxToGlobalChordIdx(manualSecondaryChord[0])
            manualSecondaryChordDict[str(globalChordlIdx)] = {
                "root": manualSecondaryChord[1],
                "target": manualSecondaryChord[2],
                "accidentalRoot": manualSecondaryChord[3] if len(manualSecondaryChord) > 3 else None,
                "accidentalTarget": manualSecondaryChord[4] if len(manualSecondaryChord) > 3 else None,
            }
        return manualSecondaryChordDict

    def _makeManualRomanNumeralDict(self, manualRomanNumerals):
        manualRomanNumeralDict = {}
        for manualRomanNumeral in manualRomanNumerals:
            globalChordlIdx = self._measureChordIdxToGlobalChordIdx(manualRomanNumeral[0])
            manualRomanNumeralDict[str(globalChordlIdx)] = {
                "numeral": manualRomanNumeral[1],
                "accidental": manualRomanNumeral[2] if len(manualRomanNumeral) > 2 else None,
            }
        return manualRomanNumeralDict

    def _measureChordIdxToGlobalChordIdx(self, measureChordIdx):
        globalChordIdx = 0
        for measure in self.streamObj[music21.stream.Measure]:
            if measure.number == measureChordIdx[0]:
                return globalChordIdx + measureChordIdx[1]
            globalChordIdx += len(measure[music21.harmony.ChordSymbol])



    @staticmethod
    def _isMajor(chordSymbol):
        notes = chordSymbol.notes
        root = chordSymbol.root()
        for note in notes:
            triadInterval = note.pitch.ps - root.ps
            if triadInterval == 4:
                return True
        return False


    @staticmethod
    def _hasDominantSeventh(chordSymbol):
        notes = chordSymbol.notes
        root = chordSymbol.root()
        for note in notes:
            interval = note.pitch.ps - root.ps
            if interval == 10:
                return True
        return False

    @staticmethod
    def _rootEqualsBass(chordSymbol):
        if chordSymbol.bass() is not None:
            if chordSymbol.root().name != chordSymbol.bass().name:
                return False
        return True

    @staticmethod
    def _isDiatonic(chordSymbol, key):  # ?unused
        majorDiatonicChords = {
            "1": [0, 4, 7, 11],
            "2": [2, 5, 9, 12],
            "3": [4, 7, 11, 14],
            "4": [5, 9, 12, 16],
            "5": [7, 11, 14, 17],
            "6": [9, 12, 16, 19],
            "7": [11, 14, 17, 21]
        }
        minorDiatonicChords = {
            "1": [0, 3, 7, 10],
            "2": [2, 5, 8, 12],
            "3": [3, 7, 10, 14],
            "4": [5, 8, 12, 15],
            "5": [7, 11, 14, 17],
            "6": [8, 12, 15, 19],
            "7": [10, 14, 17, 20]
        }
        if key.mode == 'major':
            diatonicChords = majorDiatonicChords
        else:
            diatonicChords = minorDiatonicChords

        pitches = [int(note.pitch.ps) for note in chordSymbol.notes]
        pitchKey = int(key.tonic.ps)

        for chord in diatonicChords.values():
            if PlotterChords._chordsEqual(chord, pitches, pitchKey):
                return True
        return False

    @staticmethod
    def _chordsEqual(relativeChord, absoluteChord, pitchKey):
        for i in range(min(len(absoluteChord), 4)):
            relativePitch = (absoluteChord[i] - pitchKey) % 12
            if relativeChord[i] % 12 != relativePitch:
                return False
        return True

    def _noTypesPrinted(self, chordSymbol):
        chordTypes = self._getTypeList(chordSymbol)
        if len(chordTypes) == 0 or chordTypes == ['major'] or chordTypes == ['minor']:
            return True
        else:
            return False

    def _getRomanNumeral(self, number, key, chordSymbol=None):
        numeral = None

        # this is done so that the target of the secondary dominant can be determined in its default mode (major/minor)
        if key.mode == 'major':
            if number == 1:
                numeral = 'I'
            if number == 2:
                numeral = 'ii'
            if number == 3:
                numeral = 'iii'
            if number == 4:
                numeral = 'IV'
            if number == 5:
                numeral = 'V'
            if number == 6:
                numeral = 'vi'
            if number == 7:
                numeral = 'vii'
        else:
            if number == 1:
                numeral = 'i'
            if number == 2:
                numeral = 'ii'
            if number == 3:
                numeral = 'III'
            if number == 4:
                numeral = 'iv'
            if number == 5:
                numeral = 'V'
            if number == 6:
                numeral = 'VI'
            if number == 7:
                numeral = 'VII'


        if chordSymbol:
            chordTypes = self._getTypeList(chordSymbol)
            if len(chordTypes) > 0:
                if chordTypes[0] == 'minor' or chordTypes[0] == 'half-diminished' or chordTypes[0] == 'diminished':
                    numeral = numeral.lower()
                else:
                    numeral = numeral.upper()

        return numeral
