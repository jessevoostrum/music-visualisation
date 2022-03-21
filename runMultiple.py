import json
import music21
from matplotlib.transforms import Bbox
from matplotlib.backends.backend_pdf import PdfPages

from Visualiser import Visualiser

dir_notes = '/Users/jvo/Dropbox/Jesse/projects/music_software/IFR_animation/notes/'

filename_bass = 'sample_songs_bass.txt'
filename_standards = 'sample_songs.txt'

dir_songs_bass = "/Users/jvo/Dropbox/Jesse/music/bladmuziek/bass_lines_SBL/"
dir_songs_standards = "/Users/jvo/Dropbox/Jesse/music/bladmuziek/standards_musescore/"

f = open('settings.json')
settings = json.load(f)


if False:
    path_note = dir_notes + filename_standards
    path_songs = dir_songs_standards

else:
    path_note = dir_notes + filename_bass
    path_songs = dir_songs_bass
    settings["offsetLineMax"] = 8
    settings["subdivision"] = 2


with open(path_note) as f:
    lines = f.readlines()

for line in lines:

    print(line)

    line = line.rstrip('\n')

    streamObj = music21.converter.parse(path_songs + line)

    vis = Visualiser(streamObj, settings)
    vis.plot()

    title = vis.PlotterMetadata._getSongTitle()
    figs = vis.CanvasCreator.getFigs()

    settings["heightTitle"] = 0.65
    vPosLowest = vis.CanvasCreator.getYPosLineBase(-1)

    with PdfPages(f"output/{title}.pdf") as pdf:
        for fig in figs:
            yPosLowest = vis.CanvasCreator.getYPosLineBase(-1)
            yLengthAboveTitle = 1 - vis.settings["yPosTitle"]
            if len(figs) == 1 and vPosLowest >= 0.55:
                heightStart = settings["heightA4"] * (yPosLowest - yLengthAboveTitle)
                bbox = Bbox([[0, heightStart], [settings["widthA4"], settings["heightA4"]]])
                pdf.savefig(fig, bbox_inches=bbox)
            else:
                pdf.savefig(fig)

    import matplotlib.pyplot as plt
    plt.close("all")