import fileinput
from itertools import product

grid = {}
for i, line in enumerate(fileinput.input(encoding="utf-8")):
    x,y,z = map(int, line.split(","))
    grid[x,y,z] = i

def neighbors(x, y, z):
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1

def part1(grid):
    res = 0
    for c in grid:
        s = sum(1 for cn in neighbors(*c) if cn in grid)
        res += (6 - s)
    return res

print(part1(grid))

