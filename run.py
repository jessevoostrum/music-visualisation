import os
import json
import argparse

from sample.main import Visualiser


parser = argparse.ArgumentParser()

parser.add_argument("pathSong", nargs='?', default="example/All_Of_Me.mxl")
parser.add_argument("dirOutput")

parser.add_argument("-b", "--bass", action="store_true")
parser.add_argument("-r", "--realbookFont", action="store_true")


args = parser.parse_args()


f = open('sample/settings.json')
settings = json.load(f)

if args.bass:
    settings["measuresPerLine"] = 2
    settings["subdivision"] = 2
    settings['thickBarlines'] = False

if args.realbookFont:
    settings['fontDirectory'] = "sample/fonts/Realbook"
    settings['font'] = 'Realbook'

vis = Visualiser(args.pathSong, settings)
vis.generate(args.dirOutput + '/')


