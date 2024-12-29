import music21

def preprocessStreamObj(streamObj):
    # streamObj = self._removeBassStaff(streamObj)
    # streamObj = _correctPickupMeasure(streamObj)

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
