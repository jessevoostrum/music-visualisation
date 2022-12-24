from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


vDist = 0.0015  # TODO(make dependent on barSpace)
hDist = 0.004
vShift = np.array([0, vDist])
hShift = np.array([hDist, 0])
vShiftAux = np.array([0, 0.4 * vDist])
hShiftAux = np.array([0.5 * hDist, 0])


def Parallelogram(leftBottom, leftTop, rightBottom, rightTop, alpha, facecolor, hatch, shape='straight'):
    if shape == 'rounded':
        path = RoundedPath(leftBottom, leftTop, rightBottom, rightTop)
    elif shape == 'leftRounded':
        path = LeftRoundedPath(leftBottom, leftTop, rightBottom, rightTop)
    elif shape == 'rightRounded':
        path = RightRoundedPath(leftBottom, leftTop, rightBottom, rightTop)
    elif shape == 'straight':
        path = StraightPath(leftBottom, leftTop, rightBottom, rightTop)
    else:
        print("undefined shape")
        return

    patch = patches.PathPatch(path, facecolor=facecolor, alpha=alpha, hatch=hatch, lw=0)
    return patch


def RoundedPath(leftBottom, leftTop, rightBottom, rightTop):
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

def LeftRoundedPath(leftBottom, leftTop, rightBottom, rightTop):
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

def RightRoundedPath(leftBottom, leftTop, rightBottom, rightTop):

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

def StraightPath(leftBottom, leftTop, rightBottom, rightTop):

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
