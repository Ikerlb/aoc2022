import fileinput
from itertools import product
from collections import deque

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

def part2(grid):
    mnx = min(x for x,_,_ in grid) - 1
    mxx = max(x for x,_,_ in grid) + 1
    mny = min(y for _,y,_ in grid) - 1
    mxy = max(y for _,y,_ in grid) + 1
    mnz = min(z for _,_,z in grid) - 1
    mxz = max(z for _,_,z in grid) + 1
    q = deque()

    # z axis fixed
    for x, y in product(range(mnx, mxx + 1), range(mny, mxy + 1)):
        q.append((x, y, mnz))
        q.append((x, y, mxz))

    # y axis fixed
    for x, z in product(range(mnx, mxx + 1), range(mnz, mxz + 1)):
        q.append((x, mny, z))
        q.append((x, mxy, z))

    # x axis fixed
    for y, z in product(range(mny, mxy + 1), range(mnz, mxz + 1)):
        q.append((mnx, y, z))
        q.append((mxx, y, z))

    seen = {c for c in q}
    boundary = set()
    while q:
        for _ in range(len(q)):
            x, y, z = q.popleft()
            for nx, ny, nz in neighbors(x, y, z):
                if not mnx <= nx <= mxx:
                    continue
                if not mny <= ny <= mxy:
                    continue
                if not mnz <= nz <= mxz:
                    continue
                if (nx, ny, nz) in grid:
                    boundary.add((nx, ny, nz))
                elif (nx, ny, nz) not in seen:
                    #print(x, y, z, "->", nx, ny, nz)
                    seen.add((nx, ny, nz))
                    q.append((nx, ny, nz))
    res = 0
    for c in boundary:
        s = sum(1 for cn in neighbors(*c) if cn in seen)
        res += s
    return res    


def part1(grid):
    res = 0
    for c in grid:
        s = sum(1 for cn in neighbors(*c) if cn in grid)
        res += (6 - s)
    return res

print(part1(grid))
print(part2(grid))
