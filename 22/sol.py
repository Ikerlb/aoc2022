import fileinput
from math import inf
from itertools import groupby, product

lines = [line[:-1] for line in fileinput.input(encoding = 'utf-8')]

path = lines.pop()

lines.pop() # burn



def _next_p1(g, by_row, by_col, r, c, dr, dc):
    if (dr, dc) == (0, -1) and (c - 1) < by_row[r][0]:
        return r, by_row[r][1]
    if (dr, dc) == (0, 1) and (c + 1) > by_row[r][1]:
        return r, by_row[r][0]
    if (dr, dc) == (-1, 0) and (r - 1) < by_col[c][0]:
        return by_col[c][1], c
    if (dr, dc) == (1, 0) and (r + 1) > by_col[c][1]:
        return by_col[c][0], c
    return r + dr, c + dc

def _next_p2(g, wrap, r, c, dr, dc):
    if (r + dr, c + dc) in wrap:
        res =  wrap[r + dr, c + dc]
        #print(f"succesfully wrapped {r} {c} {dr} {dc} to {res}")
        return res
    #print(f"didn't wrap {r} {c} {dr} {dc} now in {r+dr} {c+dc}")
    return r + dr, c + dc, dr, dc

def step_p2(g, wrap, r, c, dr, dc):
    nr, nc, ndr, ndc = _next_p2(g, wrap, r, c, dr, dc)
    if g[nr, nc] == "#":
        return r, c, dr, dc
    return nr, nc, ndr, ndc

def step_p1(g, by_row, by_col, r, c, dr, dc):
    nr, nc = _next_p1(g, by_row, by_col, r, c, dr, dc)
    if g[nr, nc] == "#":
        return r, c
    return nr, nc

def steps_p1(grid, by_row, by_col, r, c, dr, dc, path):
    for num, g in groupby(path, key = lambda x: x.isdigit()):
        s = "".join(g)
        if num:
            for _ in range(int(s)):
                r, c = step_p1(grid, by_row, by_col, r, c, dr, dc)
        elif s == "R":
            dr, dc = dc, -dr
        elif s == "L":
            dr, dc = -dc, dr
    return r, c, dr, dc

def fmt(lines, fmt_d):
    res = []
    for r in range(len(lines)):
        row = []
        for c in range(len(lines[r])):
            row.append(fmt_d.get((r, c), lines[r][c]))
        res.append("".join(row))
    return "\n".join(res)

def fmt_dir(dr, dc):
    if (dr, dc) == (0, 1):
        return ">"
    if (dr, dc) == (1, 0):
        return "v"
    if (dr, dc) == (0, -1):
        return "<"
    if (dr, dc) == (-1, 0):
        return "^"

def steps_p2(grid, wrap, r, c, dr, dc, path):
    fmt_d = {}
    for num, g in groupby(path, key = lambda x: x.isdigit()):
        s = "".join(g)
        if num:
            for _ in range(int(s)):
                r, c, dr, dc = step_p2(grid, wrap, r, c, dr, dc)
                fmt_d[r, c] = fmt_dir(dr, dc)
        elif s == "R":
            dr, dc = dc, -dr
            #print("turned to the right", dr, dc)
            fmt_d[r, c] = fmt_dir(dr, dc)
        elif s == "L":
            dr, dc = -dc, dr
            #print("turned to the left", dr, dc)
            fmt_d[r, c] = fmt_dir(dr, dc)
    print(fmt(lines, fmt_d))
    return r, c, dr, dc


def facing(dr, dc):
    if (dr, dc) == (0, 1):
        return 0
    if (dr, dc) == (1, 0): 
        return 1
    if (dr, dc) == (0, -1):
        return 2
    if (dr, dc) == (-1, 0):
        return 3

def rotate_180(lines):
    mx = max(len(line) for line in lines)
    tmp = [line.ljust(mx) for line in lines]
    return [line[::-1] for line in tmp[::-1]]

def find(lines, s):
    for row, line in enumerate(lines):
        try:
            if line.index(s) != -1:
                return row, line.index(s)
        except:
            continue
    return -1, -1

def interval(l):
    mn, mx = inf, -inf
    for i, e in enumerate(l):
        if e != " ":
            mn = min(mn, i)
            mx = max(mx, i)
    return mn, mx

#print(fmt(lines, {}))

# p1
sr, sc = 0, lines[0].index(".")
dr, dc = 0, 1

grid = {}

for r in range(len(lines)):
    for c in range(len(lines[r])):
        if lines[r][c] == ' ':
            continue
        grid[r, c] = lines[r][c]

by_row = [interval(row) for row in lines]
by_col = [interval(list(lines[r][c] for r in range(len(lines)) if c < len(lines[r]))) for c in range(len(lines[0]))]

r, c, dr, dc = steps_p1(grid, by_row, by_col, sr, sc, dr, dc, path)
print((1000 * (r + 1)) + (4 * (c + 1)) + facing(dr, dc))

# p2
N = int((sum(sum(1 for c in line if c != " ") for line in lines) // 6) ** 0.5)

wrap = {}
for ci in range(N):

    wrap[N - 1, ci] = (0, 2*N + (N - 1 - ci), 1, 0) # 2 -> 1 CHECK
    wrap[2*N, ci] = (3*N-1, 2*N + (N - 1 - ci), -1, 0) # 2 -> 5 CHECK

    c_0 = N + ci
    wrap[N - 1, c_0] = (ci, 2*N, 0, 1)  # 3 -> 1 CHECK
    wrap[2*N, c_0] = (2*N + (N - 1 - ci), 2*N, 0, 1)  # 3 -> 5 CHECK

    c_1 = 2 * N + ci
    wrap[-1, c_1]  = (N, N - 1 - ci, 1, 0)      # 1 -> 2 CHECK
    wrap[3*N, c_1] = (2*N - 1, N - 1 - ci, -1, 0) # 5 -> 2 CHECK

    c_2 = 3 * N + ci
    wrap[2*N - 1, c_2] = (N + (N - 1 - ci), 3 * N - 1, 0, -1) # 6 -> 4 CHECK
    wrap[3*N, c_2] = (N + (N - 1 - ci), 0, 0, 1)          # 6 -> 2 CHECK

for ri in range(N):
    
    wrap[ri, 2*N - 1] = (N, N + ri, 1, 0) # 1 -> 3
    wrap[ri, 3*N] = (2*N + (N - 1 - ri), 4*N - 1, 0, -1) # 1 -> 6

    r_0 = N + ri
    wrap[r_0, -1] = (3*N - 1, 3*N + (N - 1 - ri), -1, 0) # 2 -> 6
    wrap[r_0, 3*N] = (2*N, 3*N + (N - 1 - ri), 1, 0) # 4 -> 6

    r_1 = 2 * N + ri
    wrap[r_1, 2*N - 1] = (2*N - 1, N + (N - 1 - ri), -1, ) # 5 -> 3
    wrap[r_1, 4*N] = (N - 1 - ri, 3*N - 1, 0, -1) # 6 -> 1

sr, sc = 0, lines[0].index(".")
dr, dc = 0, 1

print(path)

r, c, dr, dc = steps_p2(grid, wrap, sr, sc, dr, dc, path)
print(r, c, dr, dc)
print((1000 * (r + 1)) + (4 * (c + 1)) + facing(dr, dc))
