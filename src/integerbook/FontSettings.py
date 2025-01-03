import json
import os


class FontSettings:

    def __init__(self, font, fontSizeType):

        pathFontDimensions = os.path.join(os.path.dirname(__file__), 'fontSettings.json')
        f = open(pathFontDimensions)
        fontSettings = json.load(f)
        if font in fontSettings.keys():
            fontSettings = fontSettings[font]
        else:
            fontSettings = fontSettings['DejaVu Sans']
            print("no fontsettings available")


        self.widthCharacter = fontSettings['widthCharacterRelative'] * fontSizeType
        self.widthMinus = fontSettings['widthMinusRelative'] * fontSizeType
        self.accidentalSpace = fontSettings['accidentalSpaceRelative'] * fontSizeType
        self.accidentalSizeRelative = fontSettings["accidentalSizeRelative"]
        self.widthDelta = fontSettings["widthDeltaRelative"] * fontSizeType
        self.widthCircle = fontSettings["widthCircleRelative"] * fontSizeType
        self.spaceAfterAddSus = fontSettings["spaceAfterAddSusRelative"] * fontSizeType
        self.accidentalXPositionRelative = fontSettings["accidentalXPositionRelative"]
        self.hDistanceChordAddition = fontSettings['hDistanceChordAdditionRelative'] * fontSizeType
        self.positionSlashRelative = fontSettings["positionSlashRelative"]
        self.widthAccidentalSlash = fontSettings["widthAccidentalSlashRelative"] * fontSizeType
