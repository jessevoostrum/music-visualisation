from PyPDF2 import PdfReader
from string import Template

dirStandards = '/Users/jvo/Documents/music-visualisation/output-standards/'

with open('notes/standards-pdf.txt', 'r') as reader:
    lines = reader.readlines()


s1 = Template('\includepdf[pages= $numPage,  pagecommand={\\vspace*{-4.2cm}\phantomsection\\addcontentsline{toc}{section}{\\normalfont{$title}}}]{$path}')
s2 = Template('\includepdf[pages= $numPage, pagecommand={}]{$path}')

with open('inputTexFile.txt', 'w') as writer:

    for line in lines:
        line = line.rstrip('\n')
        titleSong = line.rstrip('.pdf')
        pathSong = dirStandards + line
        stringFirst = s1.substitute(numPage=1, title=titleSong, path=pathSong)
        writer.write(f'{stringFirst}\n')

        reader = PdfReader(pathSong)
        numPages = len(reader.pages)

        if numPages > 1:
            stringSecond = s2.substitute(numPage='2-', path=pathSong)
            writer.write(f'{stringSecond}\n')


