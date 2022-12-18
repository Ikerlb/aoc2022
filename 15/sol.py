from sys import stdin
from collections import defaultdict
import re

# ofc, swap coords to use r, c instead of x, y
def parse(line):
    coordinates = re.findall(r'x=(-?\d+), y=(-?\d+)', line)
    return list((int(y), int(x)) for x, y in coordinates)

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# row, (cols, cole)
def generate_intervals(sp, bp):
    sr, sc = sp
    br, bc = bp
    d = manhattan_distance(sp, bp)

    yield sr, (sc - d, sc + d)

    for dr in range(1, d + 1):
        yield sr + dr, (sc - d + dr, sc + d - dr + 1)
        yield sr - dr, (sc - d + dr, sc + d - dr + 1)

def format(rows, beacons):
    mn_r, mx_r = min(rows.keys()), max(rows.keys())
    mn_c = min(c for l in rows.values() for p in l for c in p)
    mx_c = max(c for l in rows.values() for p in l for c in p)

    print(mn_r, mx_r, mn_c, mx_c)

    delta = 5
    res = []
    for r in range(mn_r - delta, mx_r + delta + 1):
        row = [f"{str(r).ljust(4)}"]
        for c in range(mn_c - delta, mx_c + delta + 1):
            if (r, c) in beacons:
                row.append('B')
            elif any(c1 <= c < c2 for c1, c2 in rows[r]):
                row.append('#')
            else:
                row.append('.')
        res.append("".join(row))
    return "\n".join(res)

def merge(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    return merged

lines = [parse(line) for line in stdin]
rows = defaultdict(list)
beacons = set()
for sp, bp in lines:
    beacons.add(bp)
    for r, inter in generate_intervals(sp, bp):
        rows[r].append(inter)

for row in rows:
    rows[row] = merge(rows[row])

def part1(rows, row):
    res = s = 0
    for c1, c2 in rows[row]:
        res += c2 - c1
        s += sum(1 for br, bc in beacons if br == row and c1 <= bc < c2)
    return res - s

def part2(rows, lo, hi):
    for r in range(lo, hi + 1):
        if r not in rows:
            continue
        prev = rows[r][0]
        for c1, c2 in rows[r][1:]:
            if c1 - prev[1] == 1 and lo <= c1 - 1 <= hi:
                return (c1 - 1) * hi + r
            prev = (c1, c2)
    return None

print(part1(rows, 10))
print(part2(rows, 0, 4000000))
