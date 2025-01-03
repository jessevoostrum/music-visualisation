import music21

def preprocessStreamObj(streamObj, Settings):
    streamObj = _makeKeySignatureIntoKey(streamObj)
    streamObj = _makeKeysMinor(streamObj, Settings.forceMinor)
    streamObj = _addKeyWhenKeyIsMissing(streamObj)
    # streamObj = self._removeBassStaff(streamObj)
    streamObj = _correctPickupMeasure(streamObj)
    streamObj = _removeSecondChordSymbolInSamePlace(streamObj)
    return streamObj


def _removeSecondChordSymbolInSamePlace(streamObj):
    for measure in streamObj[music21.stream.Measure]:
        lastChordSymbol = None
        for chordSymbol in measure[music21.harmony.ChordSymbol]:
            if lastChordSymbol:
                if chordSymbol.offset == lastChordSymbol.offset:
                    measure.remove(chordSymbol)
                    print('removed chord symbol', chordSymbol)
            lastChordSymbol = chordSymbol
    return streamObj

def _makeKeySignatureIntoKey(streamObj):
    for measure in streamObj[music21.stream.Measure]:
        for keyOrKeySignature in measure[music21.key.KeySignature]:
            if type(keyOrKeySignature) == music21.key.KeySignature:
                offset = keyOrKeySignature.offset
                newKey = keyOrKeySignature.asKey()
                measure.remove(keyOrKeySignature)
                measure.insert(offset, newKey)
                print('mode key missing')
    return streamObj

def _makeKeysMinor(streamObj, forceMinor):
    for measure in streamObj[music21.stream.Measure]:
        for key in measure[music21.key.Key]:
            if key.mode == 'major' and forceMinor:
                offset = key.offset
                newKey = key.relative
                measure.remove(key)
                measure.insert(offset, newKey)
    return streamObj
def _addKeyWhenKeyIsMissing(streamObj):
    if len(streamObj[music21.key.KeySignature]) == 0:
        print('no key specified')
        try:
            key = self.streamObj.analyze('key')
        except:
            key = music21.key.Key('C')
            print('key analysis failed')
        streamObj[music21.stream.Measure].first.insert(key)

    return streamObj



def _removeBassStaff(streamObj):
    staffs = streamObj[music21.stream.PartStaff]
    if staffs:
        if len(staffs) > 1:
            streamObj.remove(staffs[1])
            print("removed staff")

    parts = streamObj[music21.stream.Part]
    if parts:
        if len(parts) > 1:
            streamObj.remove(parts[1:])
            print("removed part(s)")

    return streamObj


def _correctPickupMeasure(streamObj):
    measures = streamObj[music21.stream.Measure]
    if measures[0].number == 1:
        if measures[0].quarterLength < measures[1].quarterLength:
            streamObj = _renumberMeasures(streamObj)
    return streamObj


def _renumberMeasures(streamObj):
    measures = streamObj[music21.stream.Measure]
    for i in range(len(measures)):
        measures[i].number = i
    return streamObj
