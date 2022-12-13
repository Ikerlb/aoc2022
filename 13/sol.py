from sys import stdin
from functools import cmp_to_key

def pair(s):
    return list(eval(p) for p in s.splitlines())

lines = "".join(line for line in stdin)

pairs = [pair(ll) for ll in lines.split("\n\n")]

def compare(p1, p2):
    i  = j = 0
    while i < len(p1) and j < len(p2): 
        e1, e2 = p1[i], p2[j]
        if type(e1) == type(e2) == int and e1 == e2:
            i += 1
            j += 1
            continue
        elif type(e1) == type(e2) == int:
            return -1 if e1 < e2 else 1 
        elif type(e1) == type(e2) == list: 
            c = compare(e1, e2)
            if c != 0:
                return c
            i += 1
            j += 1
        elif type(e1) == int:
            c = compare([e1], e2)
            if c != 0:
                return c
            i += 1
            j += 1
        else:
            c = compare(e1, [e2])
            if c != 0:
                return c
            i += 1
            j += 1
    if i == len(p1) and j == len(p2):
        return 0
    elif i == len(p1):
        return -1
    else:
        return 1

# p1
print(sum(i for i, ps in enumerate(pairs, 1) if compare(*ps) < 0))

# p2
l = [pp for p in pairs for pp in p] + [[[2]], [[6]]]
s = sorted(l, key = cmp_to_key(compare))
print((s.index([[2]]) + 1) * (s.index([[6]]) + 1))
