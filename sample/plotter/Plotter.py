import music21

class Plotter:

    def __init__(self, streamObj, Settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.Settings = Settings
        self.LocationFinder = LocationFinder
        self.axs = axs

    def _plotAccidental(self, accidental, fontSize, xPos, yPos, page, front=True):
        if accidental:
            symbolAccidental = None
            if accidental.name == 'sharp':
                symbolAccidental = '♯'
            elif accidental.name == 'flat':
                symbolAccidental = '♭'

            relativeLocation = 0.2
            if not front:
                relativeLocation = 1 - relativeLocation

            xPosAccidental = xPos + relativeLocation * self.Settings.widthNumberRelative * fontSize

            if symbolAccidental:
                self.axs[page].text(xPosAccidental,
                                    yPos + 0.7 * self.Settings.capsizeNumberRelative * fontSize, symbolAccidental,
                                    fontsize=self.Settings.fontSizeAccidentalRelative * fontSize,
                                    va='baseline', ha='right', fontname=self.Settings.font, #fontweight=1
                                    )


    def _getKeyLetter(self, key):
        letter = key.tonic.name[0]
        accidental = key.tonic.accidental
        if accidental:
            if accidental.name == 'sharp':
                letter = letter + "{}^\\#"
            elif accidental.name == 'flat':
                letter = letter + "{}^b"

        if key.mode == 'minor':
            letter += '-'

        letter = f"$\\mathregular{{{letter}}}$"

        return letter
