import json
import argparse

from sample.main import Visualiser


parser = argparse.ArgumentParser()

parser.add_argument("pathSong")
parser.add_argument("dirOutput")

parser.add_argument("-b", "--bass", action="store_true")

args = parser.parse_args()


f = open('sample/settings.json')
settings = json.load(f)

if args.bass:
    settings["measuresPerLine"] = 2
    settings["subdivision"] = 2
    settings['thickBarlines'] = False

vis = Visualiser(args.pathSong, settings)
vis.generate(args.dirOutput)


