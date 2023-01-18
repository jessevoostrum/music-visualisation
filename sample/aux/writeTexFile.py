from PyPDF2 import PdfReader
from string import Template
import glob
import os

dirStandards = '/Users/jvo/Documents/music-visualisation/output/output-standards/'

lines = glob.glob(dirStandards + '*' + '.pdf')
lines = [os.path.basename(line) for line in lines]
lines.sort()

# with open('notes/standards-pdf.txt', 'r') as reader:
#     lines = reader.readlines()

s0 = Template('\includepdf[pages= $numPage,  pagecommand={\\vspace*{-4.2cm}\phantomsection\\addcontentsline{toc}{section}{$letter} \\vspace*{-4.2cm}\phantomsection\\addcontentsline{toc}{subsection}{$title}}]{$path}')
s1 = Template('\includepdf[pages= $numPage,  pagecommand={\\vspace*{-4.2cm}\phantomsection\\addcontentsline{toc}{subsection}{$title}}]{$path}')
s2 = Template('\includepdf[pages= $numPage, pagecommand={}]{$path}')

with open('inputTexFile.txt', 'w') as writer:

    firstLetter = '_'
    for line in lines:
        line = line.rstrip('\n')
        pathSong = dirStandards + line
        titleSong = line.removesuffix('.pdf')
        if titleSong[0] != firstLetter:
            firstLetter = titleSong[0]
            stringFirst = s0.substitute(numPage=1, letter=firstLetter, title=titleSong, path=pathSong)
        else:
            stringFirst = s1.substitute(numPage=1, title=titleSong, path=pathSong)
        writer.write(f'{stringFirst}\n')

        reader = PdfReader(pathSong)
        numPages = len(reader.pages)

        if numPages > 1:
            stringSecond = s2.substitute(numPage='2-', path=pathSong)
            writer.write(f'{stringSecond}\n')

