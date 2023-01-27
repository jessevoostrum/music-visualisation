import music21
import sample.aux.chordTypes as chordTypes
from sample.plotter.Plotter import Plotter


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

                self._plotAddition(chord, xPos, yPos, page)

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


    def _plotAddition(self, chordSymbol, xPos, yPos, page):

        addition = self._findAddition(chordSymbol)

        fontSize = self.Settings.fontSizeChords
        widthNumber = self.Settings.widthNumberRelative * fontSize

        if addition:
            self.axs[page].text(xPos + widthNumber + self.Settings.hDistanceChordAddition,
                            yPos + self.Settings.capsizeNumberRelative * fontSize * 0.7, addition,
                            fontsize=self.Settings.fontSizeAccidentalRelative * fontSize,
                            va='baseline', ha='left',
                            # fontname='Arial',
                            fontweight=1)


    def _findAddition(self, chordSymbol):
        addition = ""
        
        kind = chordSymbol.chordKind

        if kind in music21.harmony.CHORD_ALIASES:
            kind = music21.harmony.CHORD_ALIASES[kind]

        if kind in music21.harmony.CHORD_TYPES:
            addition += chordTypes.getAbbreviationListGivenChordType(kind)[0]

        for csMod in chordSymbol.chordStepModifications:
            if csMod.interval is not None:
                numAlter = csMod.interval.semitones
                if numAlter > 0:
                    s = '\\#\!'
                else:
                    s = 'b'
                prefix = s * abs(numAlter)
                if abs(numAlter) > 0:
                    prefix = '\,{{}}^' + prefix

                # print("numAlter", numAlter, "\n", "prefix", prefix)

                # addition += ' ' + csMod.modType + ' ' + prefix + str(csMod.degree)
                addition += prefix + str(csMod.degree)
            else:
                # addition += ' ' + csMod.modType + ' ' + str(csMod.degree)
                addition += str(csMod.degree)

        if not addition == "":
            addition  = "$" + addition + "$"
        else:
            addition = None

        return addition

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

                # self.axs[page].text(xPos + (1 + self.Settings.hDistanceChordAddition) * self.Settings.widthNumberRelative * fontSize,
                #                     yPos + self.Settings.capsizeNumberRelative * fontSize * 0.3,
                #                     bass,
                #                     fontsize=self.Settings.fontSizeAccidentalRelative * fontSize,
                #                     va='top', ha='left',
                #                     )


    def _getNumberWithAccidental(self, chordSymbol):

        key = self.Settings.getKey(chordSymbol.getOffsetInHierarchy(self.streamObj))

        pitch = chordSymbol.bass()
        number, alteration = key.getScaleDegreeAndAccidentalFromPitch(pitch)
        number = str(number)

        if alteration:
            if alteration.name == 'sharp':
                number = f"{{}}^\\# {number}"
            elif alteration.name == 'flat':
                number = f"{{}}^b {number}"

        return number

    def _plotNoChord(self, xPos, yPos, page):

        self.axs[page].text(xPos, yPos, 'N.C.',
                            va='baseline', size=self.Settings.fontSizeChords)

