class Plotter:

    def __init__(self, streamObj, settings, LocationFinder, axs):

        self.streamObj = streamObj
        self.settings = settings
        self.LocationFinder = LocationFinder
        self.axs = axs

    def plotAccidental(self, accidental, fontSize, xPos, yPos, page, front=True):
        if accidental:
            symbolAccidental = None
            if accidental.name == 'sharp':
                symbolAccidental = '♯'
            elif accidental.name == 'flat':
                symbolAccidental = '♭'

            relativeLocation = 0.2
            if not front:
                relativeLocation = 1 - relativeLocation

            xPosAccidental = xPos + relativeLocation * self.settings["widthNumberRelative"] * fontSize

            if symbolAccidental:
                self.axs[page].text(xPosAccidental,
                                    yPos + 0.7 * self.settings['capsizeNumberRelative'] * fontSize, symbolAccidental,
                                    fontsize=self.settings['fontSizeAccidentalRelative'] * fontSize,
                                    va='baseline', ha='right', fontname='Vulf Mono', #fontweight=1
                                    )

