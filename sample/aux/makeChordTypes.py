import json

from music21.harmony import CHORD_TYPES



def getAdditionList(chordType):
    additions = []
    if 'minor' in chordType:
        additions.append("minor")
    if 'major' in chordType:
        additions.append("major")
    if 'half-diminished' in chordType:
        additions.append("half-diminished")
    if 'diminished' in chordType and not 'half-diminished' in chordType:
        additions.append("diminished")

    if 'seventh' in chordType:
        additions.append("seventh")
    if 'sixth' in chordType:
        additions.append("sixth")
    if 'ninth' in chordType:
        additions.append("ninth")
    if '11th' in chordType:
        additions.append("11th")
    if '13th' in chordType:
        additions.append("13th")

    if 'augmented' in chordType:
        additions.append("augmented")
    if 'flat-five' in chordType:
        additions.append("flat-five")

    if 'suspended-second' in chordType:
        additions.append("suspended-second")
    if 'suspended-fourth' in chordType:
        additions.append("suspended-fourth")

    if 'Neapolitan' in chordType:
        additions.append("Neapolitan")
    if 'Italian' in chordType:
        additions.append("Italian")
    if 'French' in chordType:
        additions.append("French")
    if 'German' in chordType:
        additions.append("German")
    if 'pedal' in chordType:
        additions.append("pedal")
    if 'power' in chordType:
        additions.append("power")
    if 'Tristan' in chordType:
        additions.append("Tristan")

    return additions


chordTypes = {}

for chordType in CHORD_TYPES.keys():
    chordTypes[chordType] = getAdditionList(chordType)

with open("chordTypes.json", "w") as write_file:
    json.dump(chordTypes, write_file, indent=0)


# maxLen = 0
# for k in CHORD_TYPES.keys():
#     if len(k) > maxLen:
#         maxLen = len(k)
#
# padding = maxLen + 2
# space = " "
# for chordType in CHORD_TYPES.keys():
#     print(f"'{chordType}', {space * (padding - len(chordType))} {getAdditionList(chordType)}")