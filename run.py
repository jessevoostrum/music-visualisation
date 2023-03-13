import os
import json
import argparse

from sample.main import Visualiser


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--pathSong", )
parser.add_argument("-o", "--dirOutput", )
parser.add_argument("-b", "--bass", action="store_true")
parser.add_argument("-r", "--realbookFont", action="store_true")
parser.add_argument("-c", "--colourNotes", action="store_true")
parser.add_argument("-l", "--lyrics", action="store_true")

args = parser.parse_args()

f = open('sample/settings.json')
settings = json.load(f)

if args.pathSong:
    pathSong = args.pathSong
else:
    pathSong = "example/All_Of_Me.musicxml"

if args.dirOutput:
    dirOutput = args.dirOutput
else:
    dirOutput = os.getcwd()

if args.bass:
    settings["measuresPerLine"] = 2
    settings["subdivision"] = 2
    settings['thickBarlines'] = False
    settings['saveCropped'] = True

if args.realbookFont:
    settings['fontDirectory'] = "sample/fonts/Realbook"
    settings['font'] = 'Realbook'

if args.colourNotes:
    settings['coloursCircleOfFifths'] = True

if args.lyrics:
    settings['lyrics'] = True

vis = Visualiser(pathSong, settings)
vis.generate(dirOutput)


