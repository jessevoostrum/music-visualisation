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
                self._plotChordNumberAndAccidental(chord, xPos, yPos, page)

                self._plotTypesAndModifications(chord, xPos, yPos, page)

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

    def _plotTypesAndModifications(self, chordSymbol, xPos, yPos, page):

        fontSize = self.Settings.fontSizeChords
        widthNumber = self.Settings.widthNumberRelative * fontSize

        xPos = xPos + widthNumber + self.Settings.fontSettings.hDistanceChordAddition
        yPos = yPos + self.Settings.capsizeChord * self.Settings.heightChordAddition

        self.fontSizeType = self.Settings.fontSettings.fontSizeType
        self.fontSizeTypeSmall = self.Settings.fontSettings.fontSizeTypeSmall
        self.width = self.Settings.fontSettings.widthCharacter
        self.accidentalSpace = self.Settings.fontSettings.accidentalSpace

        xPos = self._plotTypes(chordSymbol, xPos, yPos, page)

        self._plotModifications(chordSymbol, xPos, yPos, page)

    def _plotTypes(self, chordSymbol, xPos, yPos, page):
        chordTypes = self._getTypeList(chordSymbol)

        for i, chordType in enumerate(chordTypes):

            width = 0
            if chordType == "minor":
                width = self._plotTypeMinor(xPos, yPos, page)
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
        self.axs[page].text(xPos, yPos,
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
                            "$\\varnothing$", fontsize=8, math_fontfamily='dejavusans',
                            va='baseline', ha='left')
        return self.Settings.fontSettings.widthCircle

    def _plotTypeDiminished(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos - 0.0014,
                            "$\\circ$", fontsize=15, fontstyle='normal', math_fontfamily='cm',
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
        return self.width * 3

    def _plotModificationAlter(self, xPos, yPos, page):
        self.axs[page].text(xPos, yPos,
                            "alt", fontsize=self.fontSizeTypeSmall, fontstyle='normal',
                            va='baseline', ha='left')
        return self.width * 3

    def _getTypeList(self, chordSymbol):

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
                self._plotAccidental(accidental, fontSizeAddition, xPosBass, yPosBass, page)


    def _plotNoChord(self, xPos, yPos, page):

        self.axs[page].text(xPos, yPos, 'N.C.',
                            va='baseline', size=self.Settings.fontSizeChords)

