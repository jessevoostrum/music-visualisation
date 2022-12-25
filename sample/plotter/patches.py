from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


def Parallelogram(leftBottom, leftTop, rightBottom, rightTop, alpha=1, facecolor='blue', hatch=None, shape='straight'):

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
