import fileinput
from itertools import product
import plotly.graph_objects as go
import numpy as np
import math

lines = [line[:-1] for line in fileinput.input()]

instructions = lines.pop()
lines.pop() # burn line


class Region:
    def __init__(self, lines, sr, sc):
        self.lines = lines
        self.ul = (sr, sc)

    def __iter__(self):
        sr, sc = self.ul
        n, m = len(self.lines), len(self.lines[0])
        for r, c in product(range(n), range(m)):
            cr, cc = sr + r, sc + c
            yield cr, cc, self.lines[r][c]

    def __repr__(self):
        return "\n".join("".join(line) for line in self.lines)

def plot(xs, ys, zs):
    fig = go.Figure(data=[
        go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode = "markers"
        )
    ])
    fig.show()

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

#class Face:
#    def __init__(self, d):
#        self.d = d
#        self.mnr = self.mnc = self. = 0
#        self.mxr = self.mxc = 0
#
#
#class CubeProposal:
#    def __init__(self, faces = None):
#        self.regions = regions
#        self.faces = faces
#
#    def is_cube(self):
#        # if there are exactly 6 planes
#        # and each region's vertices repeat
#        # exactly 3 times, then it is a cube
#        for  
#
#    def neighbors():

def get_block_size(lines):
    return int((sum(sum(1 for c in line if c != " ") for line in lines) // 4) ** 0.5)

def get_regions(lines):
    N = get_block_size(lines)
    r = 0
    while r < len(lines):
        c = min(i for i, ch in enumerate(lines[r]) if ch != " ")
        while c < len(lines[r]):
            yield (r, c), (r + N - 1, c + N - 1)
            c += N
        r += N

print(lines)
N = get_block_size(lines)
regions = []

for ((sr, sc), (er, ec)) in get_regions(lines):
    print(sr, sc, er, ec)
    res = []
    for r in range(sr, er + 1):
        res.append(list(lines[r][c] for c in range(sc, ec + 1)))
    regions.append(Region(res, sr, sc))

print(regions)
