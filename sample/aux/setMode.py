import music21

song = "/Users/jvo/Library/Mobile Documents/com~apple~CloudDocs/bladmuziek/bass_lines_SBL/Signed, Sealed, Delivered I'm Yours.mxl"
line = "Signed, Sealed, Delivered I'm Yours.mxl"

outputPath = "/Users/jvo/Documents/music-visualisation/output/"

mode = 'major'

streamObj = music21.converter.parse(song)

keySignature = streamObj[music21.key.KeySignature].first()
firstMeasure = streamObj[music21.stream.Measure].first()
firstMeasure.keySignature = keySignature.asKey(mode)
streamObj.write("musicxml", outputPath + line)
