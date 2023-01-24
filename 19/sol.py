import fileinput
import re
import math
from collections import defaultdict
from functools import lru_cache

lines = "".join(fileinput.input(encoding = "utf-8"))

ORDER = ["ore", "clay", "obsidian", "geode"]

def parse(blueprint):
    lines = blueprint.split(". ")
    number = re.search(r"Blueprint (\d+)", lines[0]).group(1)
    robots = []
    for line in lines:
        robot = re.search(r"Each\s+(\w+)\s+robot", line).group(1)
        _, costs = line.split(" costs ")
        d = [0 for _ in ORDER]
        for c in costs.split(" and "):
            v, k = c.split(" ")
            d[ORDER.index(k)] = int(v)
        robots.append(tuple(d))
    return robots

blueprints = [parse(bp[:-2]) for bp in fileinput.input(encoding="utf-8")]

def add(t1s, t2s):
    return tuple(t1 + t2 for t1, t2 in zip(t1s, t2s))

def subs(t1s, t2s):
    return tuple(t1 - t2 for t1, t2 in zip(t1s, t2s))

def incr(t1, k):
    return tuple(e + (i == k) for i, e in enumerate(t1))

@lru_cache(None)
def dp(i, robs, ress, mins):
    if mins <= 0:
        return ress[-1]
    res = dp(i, robs, add(ress, robs), mins-1)
    robot = blueprints[i]
    for b in range(len(robot)):
        if all(bp <= rss for bp, rss in zip(robot[b], ress)):
            res = max(res, dp(i, incr(robs, b), add(subs(ress, robot[b]), robs), mins-1))
    return res

def dfs(robot, robs, ress, mins):
    mv = [max(rr[i] for rr in robot) for i in range(len(ORDER))]
    mv[-1] = math.inf
    s = {(robs, ress, mins)}
    res = 0
    while s:
        robs, ress, mins = s.pop()
        if mins <= 0:
            res = max(ress[-1], res)
            continue
        if any(rob > mx for mx, rob in zip(mv, robs)):
            continue
        s.add((robs, add(ress, robs), mins-1))
        for b in range(len(robot)):
            if all(bp <= rss for bp, rss in zip(robot[b], ress)):
                s.add((incr(robs, b), add(subs(ress, robot[b]), robs), mins-1))
    return res

print(blueprints)
print(dfs(blueprints[0], (1, 0, 0, 0), (0, 0, 0, 0), 24))
