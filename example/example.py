import os

from sample.main import Visualiser

path = os.getcwd()
pathToRoot = os.path.abspath(os.path.join(path, os.pardir))

pathToSong = "All_Of_Me.mxl"

vis = Visualiser(pathToSong, pathToRoot)
vis.generate()

