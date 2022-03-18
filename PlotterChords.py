import music21
import chordTypes

class PlotterChords:

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator, yMin, key):

        self.streamObj = streamObj

        self.settings = settings

        self.LocationFinder = LocationFinder

        self.axs1D = CanvasCreator.getAxs()

        self.yMin = yMin

        self.xShiftChords = settings["xShiftChordsRelative"] * CanvasCreator.getWidthAx()

        self.key = key

    def plotChords(self):
        chords = self.streamObj.flat.getElementsByClass('ChordSymbol')
        for chord in chords:
            line, xPos = self.LocationFinder.getLocation(chord.offset)
            xPos = xPos + self.xShiftChords

            self.axs1D[line].text(xPos, self.yMin, self._findFigure(chord),
                                  va='bottom', size=self.settings['fontSizeChords'], fontweight='semibold')

    def _findFigure(self, chordSymbol):

        chordNumberWithAccidental = self._getNumberWithAccidental(chordSymbol.root())
        addition = ""

        kind = chordSymbol.chordKind

        if kind in music21.harmony.CHORD_ALIASES:
            kind = music21.harmony.CHORD_ALIASES[kind]

        if kind in music21.harmony.CHORD_TYPES:
            addition += chordTypes.getAbbreviationListGivenChordType(kind)[0]

        bass = ""
        if chordSymbol.bass() is not None:
            if chordSymbol.root().name != chordSymbol.bass().name:
                bass = '/' + self._getNumberWithAccidental(chordSymbol.bass())


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

        if addition != "":
            figure = '$' + chordNumberWithAccidental + '^{' + addition + '}'+ bass + '$'
        else:
            figure = '$' + chordNumberWithAccidental + bass + '$'

        return figure

    def _getNumberWithAccidental(self, pitch):
        number, alteration = self.key.getScaleDegreeAndAccidentalFromPitch(pitch)
        number = str(number)

        if alteration:
            if alteration.name == 'sharp':
                number = f"{{}}^\\# {number}"
            elif alteration.name == 'flat':
                number = f"{{}}^b {number}"

        return number

