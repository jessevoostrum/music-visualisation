import music21


class Plotter:

    def __init__(self, streamObj, axs1D, LocationFinder, barSpace,
                 noteLowest, yMin, yMax):

        self.streamObj = streamObj
        self.axs1D = axs1D
        self.LocationFinder = LocationFinder
        self.barSpace = barSpace
        self.noteLowest = noteLowest
        self.yMin = yMin
        self.yMax = yMax

    def plot(self):
        # loop through elements in stream
        for el in self.streamObj.recurse():
            if type(el) == music21.note.Note:
                yPos = (el.pitch.ps - self.noteLowest) * self.barSpace
                offset = el.getOffsetInHierarchy(self.streamObj)
                line, xPos = self.LocationFinder.getLocation(offset)
                xLength = el.duration.quarterLength

                self.axs1D[line].barh(y=yPos,
                                      left=xPos,
                                      width=xLength,
                                      height=self.barSpace,
                                      facecolor='blue',
                                      alpha=0.2,
                                      align='edge'
                                      )
