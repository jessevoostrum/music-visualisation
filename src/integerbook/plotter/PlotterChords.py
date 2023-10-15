import music21

from integerbook.plotter.PlotterBase import Plotter


class PlotterChords(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):
        super().__init__(streamObj, settings, LocationFinder, axs)

        self.yMin = self.Settings.yMin

    def plotChords(self):
        chords = self.streamObj.flatten().getElementsByClass('ChordSymbol')
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
                if not self.Settings.romanNumerals:
                    widthNumber = self._plotChordNumberAndAccidental(chord, xPos, yPos, page)

                    self._plotTypesAndModifications(chord, xPos, yPos, page, widthNumber)

                    self._plotBass(chord, xPos, yPos, page)

                else:
                    widthNumber = self._plotRomanNumeral(chord, xPos, yPos, page, i, chords)

                    xPos = self._plotTypesAndModifications(chord, xPos, yPos, page, widthNumber)

                    self._plotSecondaryNumeral(chord, xPos, yPos, page)


            else:
                self._plotNoChord(xPos, yPos, page)

    def _plotChordNumberAndAccidental(self, chordSymbol, xPos, yPos, page):
        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.Settings.getKey(offsetEl)
        number, accidental = key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())

        chordNumber = number
        if self.Settings.romanNumerals:
            chordNumber = self._getRomanNumeral(number, key, chordSymbol)

        plottedNumber = self.axs[page].text(xPos, yPos, chordNumber,
                            va='baseline', size=self.Settings.fontSizeChords)

        renderer = self.axs[page].figure._get_renderer()
        bb = plottedNumber.get_window_extent(renderer=renderer).transformed(self.axs[page].transData.inverted())
        widthNumber = bb.width

        self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page)

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
                    width = self._plotTypeHalfDiminished(xPos, yPos, page)
                if chordType == 'diminished':
                    width = self._plotTypeDiminished(xPos, yPos, page)

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
                if chordType == 'flat-five':
                    width = self._plotTypeFlatFive(xPos, yPos, page)
                if chordType == 'suspended-second':
                    width = self._plotTypeSuspendedSecond(xPos, yPos, page)
                if chordType == 'suspended-fourth':
                    width = self._plotTypeSuspendedFourth(xPos, yPos, page)
            xPos += width
        return xPos

    def _plotModifications(self, chordSymbol, xPos, yPos, page):

        if self.Settings.chordVerbosity > 1:

            for csMod in chordSymbol.chordStepModifications:
                if csMod.interval is not None:
                    width = 0
                    if csMod.modType == 'add':
                        width = self._plotModificationAdd(xPos, yPos, page)
                    if csMod.modType == 'subtract':
                        width = self._plotModificationSubtract(xPos, yPos, page)
                    if csMod.modType == 'alter':
                        width = self._plotModificationAlter(xPos, yPos, page)

                    xPos += width

                    number = csMod.degree

                    accidental = None
                    if csMod.interval.semitones == -1:
                        accidental = music21.pitch.Accidental('flat')
                    if csMod.interval.semitones == 1:
                        accidental = music21.pitch.Accidental('sharp')

                    if accidental:
                        xPos -= 0.003

                    width = self._plotTypeAndModificationNumberAndAccidental(number, accidental, xPos, yPos, page)
                    width += 0.002

                    xPos += width
            return xPos

    def _plotTypeAndModificationNumberAndAccidental(self, number, accidental, xPos, yPos, page):

        if self.Settings.fontVShift:
            yPos += self.Settings.fontVShift * self.Settings.capsizeNumberRelative * self.fontSizeType

        width = 0
        if accidental:
            xPos += self.accidentalSpace
            width += self.accidentalSpace

        self._plotAccidental(accidental, self.fontSizeType, xPos, yPos, page)

        self.axs[page].text(xPos, yPos,
                            f"{number}", fontsize=self.fontSizeType,
                            va='baseline', ha='left')
        width += len(str(number)) * self.width

        return width

    def _plotTypeMinor(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos + 0.00005 * self.fontSizeType,
                            "-", fontsize = self.fontSizeType,
                            va='baseline', ha='left')
        return self.Settings.fontSettings.widthMinus

    def _plotTypeMajor(self, xPos, yPos, page):
        self.axs[page].text(xPos + 0.001, yPos - 0.00035,  # - 0.0005
                            "$\mathbb{\Delta}$", fontsize=self.fontSizeType,
                            va='baseline', ha='left')
        return self.Settings.fontSettings.widthDelta

    def _plotTypeHalfDiminished(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos - 0.00034,
                            "$\\varnothing$", fontsize=self.fontSizeTypeSmall, math_fontfamily='dejavusans',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.widthCircle

    def _plotTypeDiminished(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos - 0.0014,
                            "$\\circ$", fontsize=self.fontSizeType*1.5, fontstyle='normal', math_fontfamily='cm',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.widthCircle + 0.0003

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
        self._plotAccidental(accidental, self.fontSizeType, xPos, yPos, page)

        self.axs[page].text(xPos, yPos,
                            "5", fontsize=self.fontSizeType,
                            va='baseline', ha='left')
        return self.width + self.accidentalSpace

    def _plotTypeFlatFive(self, xPos, yPos, page):
        accidental = music21.pitch.Accidental('flat')
        self._plotAccidental(accidental, self.fontSizeType, xPos, yPos, page)

        self.axs[page].text(xPos, yPos,
                            "5", fontsize=self.fontSizeType,
                            va='baseline', ha='left')
        return self.width

    def _plotTypeSuspendedSecond(self, xPos, yPos, page):


        self.axs[page].text(xPos, yPos,
                            "sus", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')

        widthSus = self.Settings.fontSettings.spaceAddSus

        xPos2 = xPos + widthSus

        self.axs[page].text(xPos2, yPos,
                            "2", fontsize=self.fontSizeType, # fontstyle='normal',
                            va='baseline', ha='left')

        return self.width + widthSus

    def _plotTypeSuspendedFourth(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "sus", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')

        widthSus = self.Settings.fontSettings.spaceAddSus

        xPos4 = xPos + widthSus

        self.axs[page].text(xPos4, yPos,
                            "4", fontsize=self.fontSizeType,
                            va='baseline', ha='left')

        return self.width + widthSus

    def _plotModificationAdd(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "add", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.spaceAddSus

    def _plotModificationSubtract(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "sub", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.spaceAddSus

    def _plotModificationAlter(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "alt", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.spaceAddSus

    @staticmethod
    def _getTypeList(chordSymbol):

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
        if 'flat-five' in chordType:
            types.append("flat-five")

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

    def _plotBass(self, chordSymbol, xPos, yPos, page):

        if chordSymbol.bass() is not None:
            if chordSymbol.root().name != chordSymbol.bass().name:

                fontSizeAddition = self.Settings.fontSizeAccidentalRelative * self.Settings.fontSizeChords

                key = self.Settings.getKey(chordSymbol.getOffsetInHierarchy(self.streamObj))

                pitch = chordSymbol.bass()
                number, accidental = key.getScaleDegreeAndAccidentalFromPitch(pitch)

                # plot slash
                xPosRightOfChord = xPos + self.Settings.fontSettings.positionSlashRelative * self.Settings.widthNumberRelative * self.Settings.fontSizeChords
                yPosSlash = yPos - .4 * fontSizeAddition * self.Settings.capsizeNumberRelative

                self.axs[page].text(xPosRightOfChord, yPosSlash, '/', fontsize=fontSizeAddition,
                                    va='baseline', ha='left')

                # plot number
                xPosRightOfSlash = xPosRightOfChord + 0.8 * self.Settings.widthNumberRelative * fontSizeAddition
                xPosBass = xPosRightOfSlash
                if accidental:
                    xPosBass += self.Settings.fontSettings.widthAccidentalSlash

                yPosBass = yPosSlash - 0.25 * fontSizeAddition * self.Settings.capsizeNumberRelative

                self.axs[page].text(xPosBass, yPosBass, number, fontsize=fontSizeAddition,
                                    va='baseline', ha='left')

                # plot accidental
                self._plotAccidental(accidental, fontSizeAddition, xPosBass, yPosBass, page)


    def _plotNoChord(self, xPos, yPos, page):

        self.axs[page].text(xPos, yPos, 'N.C.',
                            va='baseline', size=self.Settings.fontSizeChords)

    def _plotRomanNumeral(self, chordSymbol, xPos, yPos, page, i, chords):

        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.Settings.getKey(offsetEl)
        number, accidental = key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())

        chordNumber = self._getRomanNumeral(number, key, chordSymbol)

        if self._secondaryDominant(chordSymbol, key):
            chordNumber = "V"

        plottedNumber = self.axs[page].text(xPos, yPos, chordNumber,
                                            va='baseline', size=self.Settings.fontSizeChords)

        renderer = self.axs[page].figure._get_renderer()
        bb = plottedNumber.get_window_extent(renderer=renderer).transformed(self.axs[page].transData.inverted())
        widthNumber = bb.width

        if not self._secondaryDominant(chordSymbol, key):
            self._plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page)

        return widthNumber

    def _plotSecondaryNumeral(self, chordSymbol, xPos, yPos, page):
        offsetEl = chordSymbol.getOffsetInHierarchy(self.streamObj)
        key = self.Settings.getKey(offsetEl)
        number, accidental = key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())
        target = self._secondaryDominant(chordSymbol, key)
        if target:
           self.axs[page].text(xPos, yPos, f"\{target}",
                                                va='baseline', size=self.Settings.fontSizeChords)
    def _secondaryDominant(self, chordSymbol, key):
        if self._isDiatonic(chordSymbol, key):
            return False
        if self._isMajor(chordSymbol):
            fifthOf = chordSymbol.root().transpose(-7)
            number, accidental = key.getScaleDegreeAndAccidentalFromPitch(fifthOf)
            if not accidental:
                return self._getRomanNumeral(number, key)
        return False


    @staticmethod
    def _isDiatonic(chordSymbol, key):
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
            print(relativeChord[i], relativePitch)
            print(i)
            print(relativeChord)
            if relativeChord[i] % 12 != relativePitch:
                print(i)
                return False
        return True
    @staticmethod
    def _isMajor(chordSymbol):
        notes = chordSymbol.notes
        root = chordSymbol.root()
        for note in notes:
            triadInterval = note.pitch.ps - root.ps
            if triadInterval == 4 or triadInterval == 5:
                return True
        return False

    def _isSecondaryDominant(self, romanNumeral):
        if romanNumeral.secondaryRomanNumeral:
            return True
        else:
            return False


    def _getRomanNumeral(self, number, key, chordSymbol=None):
        numeral = None
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
