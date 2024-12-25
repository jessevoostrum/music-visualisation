import music21.pitch


class Plotter:

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.Settings = Settings
        self.LocationFinder = LocationFinder
        self.axs = axs

    def _plotAccidental(self, accidental, fontSize, xPos, yPos, page, front=True, colorText='black'):
        if accidental:
            symbolAccidental = None
            if accidental.name == 'sharp':
                symbolAccidental = '♯'
            elif accidental.name == 'flat':
                symbolAccidental = '♭'
            elif accidental.name == 'natural':
                symbolAccidental = '♮'
            elif accidental.name == 'double-sharp':
                symbolAccidental = '♯♯'
            elif accidental.name == 'double-flat':
                symbolAccidental = '♭♭'

            relativeXLocation = self.Settings.fontSettings.accidentalXPositionRelative
            if not front:
                relativeXLocation = 1 - relativeXLocation

            xPosAccidental = xPos + relativeXLocation * self.Settings.widthNumberRelative * fontSize
            yPosAccidental = yPos + 0.7 * self.Settings.capsizeNumberRelative * fontSize

            fontSizeAccidental = self.Settings.fontSettings.accidentalSizeRelative * fontSize

            if symbolAccidental:

                self.axs[page].text(xPosAccidental, yPosAccidental, symbolAccidental,
                                    fontsize=fontSizeAccidental,
                                    va='baseline', ha='right', fontname=self.Settings.font, color=colorText)

    def getScaleDegreeAndAccidentalFromPitch(self, pitch, key):
        if self.Settings.minorFromMajorScalePerspective:
            distance = (pitch.midi - key.tonic.midi) % 12
            number = 0
            accidental = None
            if distance == 0:
                number = 1
            if distance == 1:
                number = 2
                accidental = -1
            if distance == 2:
                number = 2
            if distance == 3:
                number = 3
                accidental = -1
            if distance == 4:
                number = 3
            if distance == 5:
                number = 4
            if distance == 6:
                number = 4
                accidental = 1
            if distance == 7:
                number = 5
            if distance == 8:
                number = 6
                accidental = -1
            if distance == 9:
                number = 6
            if distance == 10:
                number = 7
                accidental = -1
            if distance == 11:
                number = 7

            if accidental:
                accidental = music21.pitch.Accidental(accidental)
            return number, accidental
        else:
            return key.getScaleDegreeAndAccidentalFromPitch(pitch)

    # used to print key of the song
    def _getKeyLetter(self, key):
        letter = key.tonic.name[0]
        accidental = key.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                letter = letter + "{}^\\#"
            elif accidental.name == 'flat':
                letter = letter + "{}^b"

        letter = f"$\\mathregular{{{letter}}}$"

        if key.mode == 'minor':
            enDash = u'\u2013'
            letter += enDash

        return letter

