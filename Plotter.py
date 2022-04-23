class Plotter:

    def __init__(self, axs):

        self.axs = axs

    def plotAccidental(self, accidental, fontSize, xPos, yPos, page):
        if accidental:
            symbolAccidental = None
            if accidental.name == 'sharp':
                symbolAccidental = '#'
            elif accidental.name == 'flat':
                symbolAccidental = 'b'

            if symbolAccidental:
                self.axs[page].text(xPos + 0.2 * self.settings["widthNumberRelative"] * fontSize,
                                    yPos + self.settings['capsizeNumberRelative'] * fontSize * 0.7, symbolAccidental,
                                    fontsize=self.settings['fontSizeAccidentalRelative'] * fontSize,
                                    va='baseline', ha='right', fontname='Arial', fontweight=1)

