from heapq import heappush, heappop
from sys import stdin
from itertools import takewhile

instructions = [line[:-1] for line in stdin]

def history(instructions):
    cycle = s = 1
    yield 1, 1
    for ins in instructions:
        if ins == "noop": 
            cycle += 1
            continue
        else:
            _, ns = ins.split(" ")
            s += int(ns)
            cycle += 2
            yield cycle, s

def x_at(history, time):
    l, r = 0, len(history) - 1
    res = 0
    while l <= r:
        m = (l + r) >> 1
        if history[m][0] <= time:
            res = history[m][1]
            l = m + 1
        else:
            r = m - 1
    return res

def chunks(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]
    

h = list(history(instructions))

# p1
print(sum(t * x_at(h, t) for t in range(20, 221, 40)))

res = []
for cycle in range(240):
    sprite = x_at(h, cycle + 1)
    res.append("#" if sprite - 1 <= cycle % 40 <= sprite + 1 else ".")

# p2
print("\n".join("".join(chunk) for chunk in chunks(res, 40)))
