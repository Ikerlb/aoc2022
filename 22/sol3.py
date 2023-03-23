import fileinput
from itertools import product
from collections import deque, Counter

lines = [line[:-1] for line in fileinput.input()]

instr = lines.pop()
lines.pop()

def neighbors(lines, r, c, boundary):
    deltas = product([0, -1, 1], repeat=2)
    next(deltas)
    for dr, dc in deltas:
        if boundary[0][0] - 1 <= r + dr <= boundary[1][0] + 1 and boundary[0][1] - 1 <= c + dc <= boundary[1][1] + 1:
            yield r + dr, c + dc

def get_borders(lines, boundary):
    s1 = tuple(map(lambda x: x - 1, boundary[0]))
    s2 = tuple(map(lambda x: x + 1, boundary[1]))
    s3 = (s1[0], s2[1])
    s4 = (s2[0], s1[1])

    start = [s1, s2, s3, s4]

    q = deque(start)
    visited = set(start)
    border = set()

    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if 0 <= r < len(lines) and 0 <= c < len(lines[r]) and lines[r][c] != ' ':
                border.add((r, c))
                continue
            for nr, nc in neighbors(lines, r, c, boundary):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
    return border

def with_boundary(lines, bounds):
    res = []
    for r in range(len(lines)):
        row = []
        for c in range(mc):
            if (r, c) in bounds:
                row.append("B")
            elif 0 <= r < len(lines) and 0 < c < len(lines[r]): 
                row.append(lines[r][c])
            else:
                row.append(" ")
        res.append("".join(row))
    return "\n".join(res)

def get_interior_vertices(lines, bounds, boundary):
    count = Counter()
    for r, c in bounds:
        for nr, nc in neighbors(lines, r, c, boundary):
            if 0 <= nr < len(lines) and 0 <= nc < len(lines[nr]) and lines[nr][nc] != ' ':
                count[(r, c)] += 1
    return [k for k, v in count.items() if v == 7]

def stitch(q, lines, bounds):
    r, c = q.popleft()
    

mr = len(lines)
mc = max(len(line) for line in lines)

# rect boundary
boundary = [(0, 0), (mr - 1, mc - 1)]

bounds = get_borders(lines, boundary)

print(with_boundary(lines, bounds))
print(get_interior_vertices(lines, bounds, boundary))
print(lines[0][7])
