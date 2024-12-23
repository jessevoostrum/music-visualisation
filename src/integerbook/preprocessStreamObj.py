import music21

def preprocessStreamObj(self, streamObj, settings):
    # streamObj = self._removeBassStaff(streamObj)
    streamObj = self._correctPickupMeasure(streamObj)

    if 'minorFromMajorScalePerspective' in settings:
        if settings["minorFromMajorScalePerspective"]:


    return streamObj


def _removeBassStaff(self, streamObj):
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


def _correctPickupMeasure(self, streamObj):
    measures = streamObj[music21.stream.Measure]
    if measures[0].number == 1:
        if measures[0].quarterLength < measures[1].quarterLength:
            streamObj = self._renumberMeasures(streamObj)
    return streamObj


def _renumberMeasures(self, streamObj):
    measures = streamObj[music21.stream.Measure]
    for i in range(len(measures)):
        measures[i].number = i
    return streamObj
