from collections import deque
from sys import stdin
from itertools import product
import math

grid = [[int(d) for d in line[:-1]] for line in stdin]

def next_largest(arr):
    res = [-1 for _ in range(len(arr))]
    s = []
    for i in range(len(arr)):
        while s and arr[s[-1]] <= arr[i]: 
            res[s.pop()] = i
        s.append(i)
    return res

def prev_largest(arr):
    res = [-1 for _ in range(len(arr))]
    s = []
    for i in range(len(arr) -1, -1, -1):
        while s and arr[s[-1]] <= arr[i]:
            res[s.pop()] = i
        s.append(i)
    return res
    
def replace(grid, ov, nv):
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == ov:
        grid[i][j] = nv
  return grid

def transpose(grid):
  return [list(row) for row in zip(*grid)]

def format(grid):
    return "\n".join("".join(map(lambda x: str(x).rjust(3), row)) for row in grid)

n, m = len(grid), len(grid[0])

l2r = [next_largest(row) for row in grid]
r2l = [prev_largest(row) for row in grid]

u2d = transpose([next_largest([grid[r][c] for r in range(n)]) for c in range(m)])
d2u = transpose([prev_largest([grid[r][c] for r in range(n)]) for c in range(m)])

def part1(l2r, r2l, u2d, d2u):
    res = 0
    for r, c in product(range(n), range(m)):
        res += -1 in [l2r[r][c], r2l[r][c], u2d[r][c], d2u[r][c]]
    return res

def part2(l2r, r2l, u2d, d2u):
    n, m = len(l2r), len(l2r[0])
    mx = -math.inf

    for r, c in product(range(n), range(m)):
        l2r[r][c] = m - 1 if l2r[r][c] == -1 else l2r[r][c]
        r2l[r][c] = 0 if r2l[r][c] == -1 else r2l[r][c]
        u2d[r][c] = n - 1 if u2d[r][c] == -1 else u2d[r][c]
        d2u[r][c] = 0 if d2u[r][c] == -1 else d2u[r][c]

        l2r_vd = l2r[r][c] - c
        r2l_vd = c - r2l[r][c]
        u2d_vd = u2d[r][c] - r
        d2u_vd = r - d2u[r][c]
        mx = max(mx, l2r_vd * r2l_vd * u2d_vd * d2u_vd)
    return mx

print(part1(l2r, r2l, u2d, d2u))
print(part2(l2r, r2l, u2d, d2u))

