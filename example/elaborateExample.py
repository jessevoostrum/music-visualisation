import json

from sample.main import Visualiser


f = open('../sample/settings.json')
settings = json.load(f)

settings["measuresPerLine"] = 2
settings["subdivision"] = 2
settings['thickBarlines'] = False

pathToSong = "Express Yourself.mxl"

vis = Visualiser(pathToSong, settings)
vis.generate()

