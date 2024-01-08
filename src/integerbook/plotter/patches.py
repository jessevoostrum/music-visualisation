import math
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

def verticesSegno():
    vertices = np.array([[7.04181487e-01, 2.42229208e-01],
       [7.04181487e-01, 1.77206670e-01],
       [6.83102518e-01, 1.21114619e-01],
       [6.40944580e-01, 7.39546126e-02],
       [5.96642921e-01, 2.46510397e-02],
       [5.42337746e-01, 3.11112602e-08],
       [4.78029055e-01, 3.11112602e-08],
       [4.34442022e-01, 3.11112602e-08],
       [3.95142275e-01, 1.32223176e-02],
       [3.60129816e-01, 3.96575571e-02],
       [3.22259165e-01, 6.82379182e-02],
       [3.03323762e-01, 1.03608312e-01],
       [3.03323762e-01, 1.45767184e-01],
       [3.03323762e-01, 2.01501454e-01],
       [3.39050847e-01, 2.29367812e-01],
       [4.10505016e-01, 2.29367812e-01],
       [4.39801092e-01, 2.29367812e-01],
       [4.59808278e-01, 2.11503725e-01],
       [4.70526419e-01, 1.75777107e-01],
       [4.86960788e-01, 1.20042836e-01],
       [5.04824408e-01, 9.21764789e-02],
       [5.24116968e-01, 9.21764789e-02],
       [5.74849481e-01, 9.21764789e-02],
       [6.00215738e-01, 1.22186402e-01],
       [6.00215738e-01, 1.82207805e-01],
       [6.00215738e-01, 4.10443136e-01],
       [2.78882910e-02, 3.84547677e-01],
       [1.08889418e-06, 7.55627257e-01],
       [1.08889418e-06, 8.19221788e-01],
       [2.10800580e-02, 8.75670063e-01],
       [6.32379961e-02, 9.24973636e-01],
       [1.05395934e-01, 9.74991212e-01],
       [1.57557388e-01, 1.00000000e+00],
       [2.19722512e-01, 1.00000000e+00],
       [2.67596678e-01, 1.00000000e+00],
       [3.09040146e-01, 9.87851052e-01],
       [3.44052605e-01, 9.63559379e-01],
       [3.83352351e-01, 9.35691465e-01],
       [4.03002224e-01, 8.98893064e-01],
       [4.03002224e-01, 8.53162620e-01],
       [4.03002224e-01, 8.29581839e-01],
       [3.93713957e-01, 8.09217962e-01],
       [3.75135245e-01, 7.92069434e-01],
       [3.57271624e-01, 7.75634910e-01],
       [3.36192655e-01, 7.67416870e-01],
       [3.11898337e-01, 7.67416870e-01],
       [2.71169495e-01, 7.67416870e-01],
       [2.42945047e-01, 7.90639872e-01],
       [2.27225148e-01, 8.37084320e-01],
       [2.12220186e-01, 8.84244327e-01],
       [1.93998942e-01, 9.07825108e-01],
       [1.72562816e-01, 9.07825108e-01],
       [1.53270256e-01, 9.07825108e-01],
       [1.37193044e-01, 8.97822837e-01],
       [1.24331182e-01, 8.77813629e-01],
       [1.11469786e-01, 8.58521535e-01],
       [1.05038621e-01, 8.38513882e-01],
       [1.05038621e-01, 8.17792226e-01],
       [1.05038621e-01, 5.91753350e-01],
       [6.78084894e-01, 6.16279914e-01],
       [7.04181487e-01, 2.42229208e-01],
       [7.04181487e-01, 2.42229208e-01],
       [7.04181487e-01, 2.42229208e-01]])
    return vertices

def Segno(xPos, yPos, height, xyRatio):

    vertices = verticesSegno()

    vertices *= height
    vertices *= np.array([1/xyRatio, 1])

    vertices += [xPos, yPos]

    codes = [ 1,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
        4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
        4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  4,
        4,  4,  4,  4,  4,  4,  4,  4,  4,  4,  2, 79]

    path = Path(vertices, codes)

    patch1 = patches.PathPatch(path, facecolor='black', linewidth=0)

    xPosEnd = vertices[:,0].max()
    widthSegno = xPosEnd - xPos
    widthLine = widthSegno * 0.1
    corners = [(xPos, yPos),
               (xPosEnd - widthLine, yPos + height),
               (xPosEnd, yPos + height),
               (xPos + widthLine, yPos)]
    patch2 = patches.Polygon(corners, fill=True, color='black', linewidth=0)
    radiusX = widthSegno * 0.1
    radiusY = radiusX * xyRatio
    offsetYCircle = 2 * radiusY
    patch3 = patches.Ellipse((xPos + radiusX, yPos + .5 * height - offsetYCircle), width=2 * radiusX, height= 2 * radiusY,
                             color='black', linewidth=0)
    patch4 = patches.Ellipse((xPos + widthSegno - radiusX, yPos + .5 * height + offsetYCircle), width=2 * radiusX, height=2 * radiusY,
                             color='black', linewidth=0)

    return [patch1, patch2, patch3, patch4]

def relativeWidthSegno():
    return verticesSegno()[:,0].max()

def Coda(xPos, yPos, height, width, xyRatio):

    diameterOuterY = height * .75
    diameterInnerY = 0.9 * diameterOuterY

    diameterOuterX = width * .7
    diameterInnerX = 0.5 * diameterOuterX

    linewidthY = 0.06 * height
    linewidthX = linewidthY / xyRatio

    xCenter = xPos + width / 2
    yCenter = yPos + height / 2

    patch1 = patches.Ellipse((xCenter, yCenter), width=diameterOuterX,
                     height=diameterOuterY, color='black', linewidth=0)
    patch2 = patches.Ellipse((xCenter, yCenter), width=diameterInnerX,
                     height=diameterInnerY, color='white', linewidth=0)

    patch3 = patches.Rectangle((xPos, yPos + .5 * height - 0.5 * linewidthY), width=width, height=linewidthY, fill=True,
                       color='black', linewidth=0)
    patch4 = patches.Rectangle((xPos + .5 * width - 0.5 * linewidthX, yPos), width=linewidthX, height=height, fill=True,
                       color='black', linewidth=0)

    return [patch1, patch2, patch3, patch4]

def Triangle(xPos, yPos, height, width, xyRatio):
    corners = [(xPos, yPos),
               (xPos + width / 2, yPos + height),
               (xPos + width, yPos)]
    patch = patches.Polygon(corners, fill=True, color='black', linewidth=0)

    angle = math.atan(height / (width / 2))
    linewidth0 = 0.06 * height  # bottom
    linewidth1 = 0.06 * height
    linewidth1 = correctLineWidthTriangle(linewidth1, xyRatio, angle)
    linewidth2 = 0.06 * height
    linewidth2 = correctLineWidthTriangle(linewidth2, xyRatio, angle)

    x0 = linewidth0 / math.tan(angle)
    x1 = linewidth1 / math.sin(angle)
    x2 = linewidth2 / math.sin(angle)

    x3 = (x1 + x2) / 2 - x1
    y3 = math.tan(angle) * ((x1 + x2) / 2)

    innerCorners = [(corners[0][0] + x1 + x0, corners[0][1] + linewidth0),
                    (corners[1][0] - x3, corners[1][1] - y3),
                    (corners[2][0] - x2 - x0, corners[2][1] + linewidth0)]
    patchInner = patches.Polygon(innerCorners, fill=True, color='white', linewidth=0)

    return patch, patchInner

def correctLineWidthTriangle(linewidth, xyRatio, angle):
    a = math.cos(angle) * linewidth
    b = math.sin(angle) * linewidth

    c_new = math.sqrt(a**2 + b**2 / xyRatio**2)

    return c_new

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