import argparse

from sample.main import Visualiser


parser = argparse.ArgumentParser()

parser.add_argument("pathSong")
parser.add_argument("dirOutput")

args = parser.parse_args()


vis = Visualiser(args.pathSong)
vis.generate(args.dirOutput)


