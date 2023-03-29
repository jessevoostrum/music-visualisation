from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


def Parallelogram(leftBottom, leftTop, rightBottom, rightTop, alpha=1, facecolor='blue', hatch=None, shape='straight'):

    leftBottom = np.array(leftBottom)
    leftTop = np.array(leftTop)
    rightBottom = np.array(rightBottom)
    rightTop = np.array(rightTop)

    deltaX = rightBottom[0] - leftBottom[0]
    deltaY = rightBottom[1] - leftBottom[1]
    if deltaX > 0:
        slope = deltaY / deltaX
    else:
        slope = 0

    vDist = 0.0015  # TODO(make dependent on barSpace)
    vDist = min(vDist, leftTop[1] - leftBottom[1])
    hDist = 0.004
    hDist = min(hDist, rightBottom[0] - leftBottom[0])
    vShift = np.array([0, vDist])
    hShift = np.array([hDist, 0]) + np.array([0, hDist * slope])
    vShiftAux = 0.4 * vShift
    hShiftAux = 0.5 * hShift

    if shape == 'rounded':
        path = RoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux)
    elif shape == 'leftRounded':
        path = LeftRoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux)
    elif shape == 'rightRounded':
        path = RightRoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux)
    elif shape == 'straight':
        path = StraightPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux)
    elif shape == 'squiggly':
        path = SquigglyPath(leftBottom, leftTop, rightBottom, rightTop)
    else:
        print("undefined shape")
        return

    patch = patches.PathPatch(path, facecolor=facecolor, alpha=alpha, hatch=hatch, lw=0)
    return patch


def RoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux):
    vertsBase = [leftBottom + vShift,
                 leftTop - vShift,
                 leftTop - vShiftAux,
                 leftTop + hShiftAux,
                 leftTop + hShift,
                 rightTop - hShift,
                 rightTop - hShiftAux,
                 rightTop - vShiftAux,
                 rightTop - vShift,
                 rightBottom + vShift,
                 rightBottom + vShiftAux,
                 rightBottom - hShiftAux,
                 rightBottom - hShift,
                 leftBottom + hShift,
                 leftBottom + hShiftAux,
                 leftBottom + vShiftAux,
                 leftBottom + vShift
                 ]

    verts = [(point[0], point[1]) for point in vertsBase]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4]

    path = Path(verts, codes)
    return path

def LeftRoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux):
    vertsBase = [leftBottom + vShift,
                 leftTop - vShift,
                 leftTop - vShiftAux,
                 leftTop + hShiftAux,
                 leftTop + hShift,
                 rightTop,
                 rightBottom,
                 leftBottom + hShift,
                 leftBottom + hShiftAux,
                 leftBottom + vShiftAux,
                 leftBottom + vShift
                 ]

    verts = [(point[0], point[1]) for point in vertsBase]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4]

    path = Path(verts, codes)
    return path

def RightRoundedPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux):

    vertsBase = [leftBottom,
                 leftTop,
                 rightTop - hShift,
                 rightTop - hShiftAux,
                 rightTop - vShiftAux,
                 rightTop - vShift,
                 rightBottom + vShift,
                 rightBottom + vShiftAux,
                 rightBottom - hShiftAux,
                 rightBottom - hShift,
                 leftBottom
                 ]

    verts = [(point[0], point[1]) for point in vertsBase]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             ]

    path = Path(verts, codes)
    return path

def StraightPath(leftBottom, leftTop, rightBottom, rightTop, vShift, hShift, vShiftAux, hShiftAux ):

    vertsBase = [leftBottom,
                 leftTop,
                 rightTop,
                 rightBottom,
                 leftBottom
                 ]

    verts = [(point[0], point[1]) for point in vertsBase]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             ]

    path = Path(verts, codes)
    return path

def SquigglyPath(leftBottom, leftTop, rightBottom, rightTop):
    numSquiggles = 20
    amplitude = .15 * (leftTop[1] - leftBottom[1])

    # squiggle params
    widthCornerSquiggleRelative = 0.4
    relativeDistanceAuxSquiggle = 0.3

    # corner params
    vDist = 0.001
    hDist = 0.001
    vRelativeDistanceAux = 0.4
    hRelativeDistanceAux = 0.5


    parityNumSquiggles = (-1) ** (numSquiggles % 2)
    lengthSquiggle = (rightBottom[0] - leftBottom[0]) / numSquiggles
    lengthHalfSquiggle = lengthSquiggle / 2
    slope = amplitude / lengthHalfSquiggle

    widthCornerSquiggle = widthCornerSquiggleRelative * lengthSquiggle

    amplitude = np.array([0, amplitude])

    vDist = min(vDist, leftTop[1] - leftBottom[1])
    hDist = min(hDist, rightBottom[0] - leftBottom[0])
    vShift = np.array([0, vDist])
    hShiftCorner = np.array([hDist, 0])
    hShiftCornerVertical = np.array([0, hDist * slope])
    vShiftAux = vRelativeDistanceAux * vShift
    hShiftCornerAux = hRelativeDistanceAux * hShiftCorner
    hShiftCornerAuxVertical = hRelativeDistanceAux * hShiftCornerVertical

    vertsBase1 = [leftBottom + vShift,
                  leftTop - vShift,
                  leftTop - vShiftAux,
                  leftTop + hShiftCornerAux + hShiftCornerAuxVertical,
                  leftTop + hShiftCorner + hShiftCornerVertical]

    vertsBase2 = vertsBasePart(leftTop, numSquiggles, lengthHalfSquiggle, amplitude, widthCornerSquiggle, slope, relativeDistanceAuxSquiggle)

    vertsBase3 = [rightTop - hShiftCorner - parityNumSquiggles * hShiftCornerVertical,
                  rightTop - hShiftCornerAux - parityNumSquiggles * hShiftCornerAuxVertical,
                  rightTop - vShiftAux,
                  rightTop - vShift,
                  rightBottom + vShift,
                  rightBottom + vShiftAux,
                  rightBottom - hShiftCornerAux - parityNumSquiggles * hShiftCornerAuxVertical,
                  rightBottom - hShiftCorner - parityNumSquiggles * hShiftCornerVertical]

    vertsBase4 = vertsBasePart(leftBottom, numSquiggles, lengthHalfSquiggle, amplitude, widthCornerSquiggle, slope, relativeDistanceAuxSquiggle, invert=True)

    vertsBase5 = [leftBottom + hShiftCorner + hShiftCornerVertical,
                  leftBottom + hShiftCornerAux + hShiftCornerAuxVertical,
                  leftBottom + vShiftAux,
                  leftBottom + vShift
                  ]

    vertsBase = vertsBase1 + vertsBase2 + vertsBase3 + vertsBase4 + vertsBase5

    verts = [(point[0], point[1]) for point in vertsBase]

    codes1 = [Path.MOVETO,
              Path.LINETO,
              Path.CURVE4,
              Path.CURVE4,
              Path.CURVE4]

    codes2 = numSquiggles * [Path.LINETO,
                             Path.CURVE4,
                             Path.CURVE4,
                             Path.CURVE4]

    codes3 = [Path.LINETO,
              Path.CURVE4,
              Path.CURVE4,
              Path.CURVE4,
              Path.LINETO,
              Path.CURVE4,
              Path.CURVE4,
              Path.CURVE4]

    codes4 = numSquiggles * [Path.LINETO,
                             Path.CURVE4,
                             Path.CURVE4,
                             Path.CURVE4]

    codes5 = [Path.LINETO,
              Path.CURVE4,
              Path.CURVE4,
              Path.CURVE4]

    codes = codes1 + codes2 + codes3 + codes4 + codes5

    path = Path(verts, codes)

    return path


def vertsBasePart(leftCorner, numSquiggles, lengthHalfSquiggle, amplitude, widthCornerSquiggle, slope, relativeDistanceAuxSquiggle, invert=False):
    hShiftSquiggle = np.array([widthCornerSquiggle / 2, 0])
    vShiftSquiggle = np.array([0, slope * hShiftSquiggle[0]])
    hShiftSquiggleAux = relativeDistanceAuxSquiggle * hShiftSquiggle
    vShiftSquiggleAux = np.array([0, slope * hShiftSquiggleAux[0]])

    vertsBasePart = []
    for i in range(numSquiggles):
        hShift = np.array([(2 * i + 1) * lengthHalfSquiggle, 0])
        isTop = (-1)**(i % 2)
        a = [leftCorner + isTop * amplitude + hShift - hShiftSquiggle - isTop * vShiftSquiggle,
             leftCorner + isTop * amplitude + hShift - hShiftSquiggleAux - isTop * vShiftSquiggleAux,
             leftCorner + isTop * amplitude + hShift + hShiftSquiggleAux - isTop * vShiftSquiggleAux,
             leftCorner + isTop * amplitude + hShift + hShiftSquiggle - isTop * vShiftSquiggle]
        vertsBasePart += a
    if invert:
        vertsBasePart = list(reversed(vertsBasePart))
    return vertsBasePart


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    width = 2
    height = .2

    leftBottom = np.array([0, 0])
    leftTop = np.array([0, height])
    rightBottom = np.array([width, 0])
    rightTop = np.array([width, height])

    fig, ax = plt.subplots()

    patch = Parallelogram(leftBottom, leftTop, rightBottom, rightTop, shape='squiggly')

    ax.set_xlim(-0.1, 3.1)
    ax.set_ylim(-1, 2.1)

    ax.add_patch(patch)

    plt.show()