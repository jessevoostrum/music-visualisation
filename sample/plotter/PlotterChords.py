import music21
import sample.chordTypes as chordTypes
from sample.plotter.Plotter import Plotter


class PlotterChords(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, axs):
        super().__init__(streamObj, settings, LocationFinder, axs)

        self.yMin = self.Settings.yMin

        self.key = self.Settings.key

    def plotChords(self):
        chords = self.streamObj.flat.getElementsByClass('ChordSymbol')
        for chord in chords:
            offset = chord.offset
            page, yPosLineBase, xPos = self.LocationFinder.getLocation(offset)

            xPos = xPos + self.Settings.xShiftChords
            yPos = self.yMin + yPosLineBase

            self._plotChordNumberAndAccidental(chord, xPos, yPos, page)

            self._plotAddition(chord, xPos, yPos, page)

            self._plotBass(chord, xPos, yPos, page)


    def _plotChordNumberAndAccidental(self, chordSymbol, xPos, yPos, page):
        number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())

        self.axs[page].text(xPos, yPos, number,
                            va='baseline', size=self.Settings.fontSizeChords)

        self.plotAccidental(accidental, self.Settings.fontSizeChords, xPos, yPos, page)


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
        bass = None

        if chordSymbol.bass() is not None:
            if chordSymbol.root().name != chordSymbol.bass().name:
                bass = '/' + self._getNumberWithAccidental(chordSymbol.bass())

        fontSize = self.Settings.fontSizeChords


        if bass:
            self.axs[page].text(xPos + (1 + self.Settings.hDistanceChordAddition) * self.Settings.widthNumberRelative * fontSize,
                            yPos + self.Settings.capsizeNumberRelative * fontSize * 0.3, bass,
                            fontsize=self.Settings.fontSizeAccidentalRelative * fontSize,
                            va='top', ha='left',
                            # fontname='Arial',
                            fontweight=1)


    def _getNumberWithAccidental(self, pitch):
        number, alteration = self.key.getScaleDegreeAndAccidentalFromPitch(pitch)
        number = str(number)

        if alteration:
            if alteration.name == 'sharp':
                number = f"{{}}^\\# {number}"
            elif alteration.name == 'flat':
                number = f"{{}}^b {number}"

        return number

