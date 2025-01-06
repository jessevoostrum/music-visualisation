import music21.pitch
import matplotlib.patheffects as path_effects

class Plotter:

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.Settings = Settings
        self.LocationFinder = LocationFinder
        self.axs = axs

    def _plotAccidental(self, accidental, fontSize, xPos, yPos, page, front=True, colorText='black', zorder=1):
        if accidental:
            symbolAccidental = accidental.unicode

            relativeXLocation = self.Settings.fontSettings.accidentalXPositionRelative
            if not front:
                relativeXLocation = 1 - relativeXLocation

            xPosAccidental = xPos + relativeXLocation * self.Settings.widthNumberRelative * fontSize
            yPosAccidental = yPos + 0.7 * self.Settings.capsizeNumberRelative * fontSize

            fontSizeAccidental = self.Settings.fontSettings.accidentalSizeRelative * fontSize

            if symbolAccidental:

                text = self.axs[page].text(xPosAccidental, yPosAccidental, symbolAccidental,
                                    fontsize=fontSizeAccidental,
                                    va='baseline', ha='right', fontname=self.Settings.font, color=colorText,
                                    zorder=zorder)

                text.set_path_effects([
                    path_effects.Stroke(linewidth=0.3, foreground='black'),  # Edge color and width
                    path_effects.Normal()  # Normal rendering on top of the stroke
                ])



    def getScaleDegreeAndAccidentalFromPitch(self, pitch, key, accidentalAsString=False):
        if key.mode == 'major':
            number, accidental = key.getScaleDegreeAndAccidentalFromPitch(pitch)
        else:
            if self.Settings.minorFromParallelMajorScalePerspective:
                number, accidental = self._getScaleDegreeAndAccidentalParralelMajor(key, pitch)
            elif self.Settings.minorFromMinorScalePerspective:
                number, accidental = key.getScaleDegreeAndAccidentalFromPitch(pitch)
            elif self.Settings.minorFromRelativeMajorScalePerspective:
                number, accidental = key.relative.getScaleDegreeAndAccidentalFromPitch(pitch)
        if accidentalAsString:
            if accidental:
                accidental = accidental.unicode
            else:
                accidental = ""
        return number, accidental

    def _getScaleDegreeAndAccidentalParralelMajor(self, key, pitch):
        number, accidental = key.getScaleDegreeAndAccidentalFromPitch(pitch)

        if number in {3, 6, 7}:
            if accidental and accidental.name == 'flat':
                number -= 1
                accidental = None
            if not accidental:
                accidental = music21.pitch.Accidental('flat')
            if accidental and accidental.name == 'sharp':
                accidental = None

        return number, accidental



# used to print key of the song
    def _getKeyLetter(self, key):

        tonicIsOne = key.mode == 'major' or not self.Settings.minorFromRelativeMajorScalePerspective

        if tonicIsOne:
            letter = key.tonic.name[0]
            accidental = key.tonic.accidental
        else:
            letter = key.relative.tonic.name[0]
            accidental = key.relative.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                letter = letter + "#"
            elif accidental.name == 'flat':
                letter = letter + "♭"

        if key.mode == 'minor' and self.Settings.minorFromMinorScalePerspective:
            enDash = u'\u2013'
            letter += enDash

        return letter

    def getKey(self, offset):
        lastKey = None
        if self.streamObj[music21.key.Key, music21.key.KeySignature]:
            for key in self.streamObj[music21.key.Key]:
                offsetKey = key.getOffsetInHierarchy(self.streamObj)
                if offset >= offsetKey:
                    lastKey = key
                else:
                    break
        return lastKey


