import music21
import chordTypes
from Plotter import Plotter


class PlotterChords(Plotter):

    def __init__(self, streamObj, settings, LocationFinder, CanvasCreator, yMin, key):
        super().__init__(CanvasCreator.getAxs())

        self.streamObj = streamObj

        self.settings = settings

        self.LocationFinder = LocationFinder
        self.CanvasCreator = CanvasCreator

        # self.axs = CanvasCreator.getAxs()

        self.yMin = yMin

        self.key = key

    def plotChords(self):
        chords = self.streamObj.flat.getElementsByClass('ChordSymbol')
        for chord in chords:
            line, offsetLine = self.LocationFinder.getLocation(chord.offset)
            xPos = self.CanvasCreator.getXPosFromOffsetLine(offsetLine) + self.settings["xShiftChords"]

            yPos = self.yMin + self.CanvasCreator.getYPosLineBase(line)
            page = self.CanvasCreator.getLinesToPage()[line]

            self._plotChordNumberAndAccidental(chord, xPos, yPos, page)

            lengthAddition = self._plotAddition(chord, xPos, yPos, page)

            self._plotBass(chord, xPos, yPos, page, lengthAddition)


    def _plotChordNumberAndAccidental(self, chordSymbol, xPos, yPos, page):
        number, accidental = self.key.getScaleDegreeAndAccidentalFromPitch(chordSymbol.root())

        self.axs[page].text(xPos, yPos, number,
                            va='bottom', size=self.settings['fontSizeChords'])

        self.plotAccidental(accidental, self.settings['fontSizeChords'], xPos, yPos, page)


    def _plotAddition(self, chordSymbol, xPos, yPos, page):

        addition = self._findAddition(chordSymbol)

        # lengthAddition = len(addition)  # does not work

        fontSize = self.settings['fontSizeChords']

        self.axs[page].text(xPos + (1 + self.settings["hDistanceChordAddition"]) * self.settings["widthNumberRelative"] * fontSize,
                            yPos + self.settings['capsizeNumberRelative'] * fontSize * 0.7, addition,
                            fontsize=self.settings['fontSizeAccidentalRelative'] * fontSize,
                            va='baseline', ha='left',
                            # fontname='Arial',
                            fontweight=1)

        # return lengthAddition

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

        addition  = "$" + addition + "$"

        return addition

    def _plotBass(self, chord, xPos, yPos, page, lengthAddition):
        pass

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

