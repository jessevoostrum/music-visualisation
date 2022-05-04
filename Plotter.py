class Plotter:

    def __init__(self, axs):

        self.axs = axs

    def plotAccidental(self, accidental, fontSize, xPos, yPos, page):
        if accidental:
            symbolAccidental = None
            if accidental.name == 'sharp':
                symbolAccidental = '♯'
            elif accidental.name == 'flat':
                symbolAccidental = '♭'

            if symbolAccidental:
                self.axs[page].text(xPos + 0.2 * self.settings["widthNumberRelative"] * fontSize,
                                    yPos + 0.7 * self.settings['capsizeNumberRelative'] * fontSize, symbolAccidental,
                                    fontsize=self.settings['fontSizeAccidentalRelative'] * fontSize,
                                    va='baseline', ha='right', fontname='Vulf Mono', #fontweight=1
                                    )

