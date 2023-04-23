import os
import json
import argparse

from integerbook.main import Visualiser


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--pathSong", )
parser.add_argument("-o", "--dirOutput", )
parser.add_argument("-d", "--settingsDict", )
parser.add_argument("-b", "--bass", action="store_true")
parser.add_argument("-c", "--colourNotes", action="store_true")
parser.add_argument("-l", "--lyrics", action="store_true")
parser.add_argument("-cn", "--chordNotes", action="store_true")
parser.add_argument("-cp", "--chordProgression", action="store_true")

args = parser.parse_args()

if args.pathSong:
    pathSong = args.pathSong
else:
    print("missing song path")
    raise SystemExit(1)

if args.dirOutput:
    dirOutput = args.dirOutput
else:
    dirOutput = os.getcwd()

if args.settingsDict:
    pathSettings = args.settingsDict
    f = open(pathSettings)
    settings = json.load(f)
else:
    settings = {}

if args.bass:
    settings["measuresPerLine"] = 2
    settings["subdivision"] = 2
    settings['thickBarlines'] = False
    settings['saveCropped'] = True

if args.colourNotes:
    settings['coloursCircleOfFifths'] = True

if args.lyrics:
    settings['lyrics'] = True
    settings['usePlt'] = True
    
if args.chordNotes:
    settings["plotChordTones"] = True

if args.chordProgression:
    settings["plotChordNotes"] = True
    settings["plotMelody"] = False
    settings["measuresPerLine"] = 8

vis = Visualiser(pathSong, settings)
vis.saveFig(dirName=dirOutput)


