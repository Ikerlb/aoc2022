from sys import stdin

def parse(line):
    a, b = line.split(" ")
    return a, int(b)

lines = [parse(line[:-1]) for line in stdin]

def update(r, l):
    match r:
        case "R":
            l[1] += 1
        case "L":
            l[1] -= 1
        case "U":
            l[0] += 1
        case "D":
            l[0] -= 1

def sign(n):
    if n == 0:
        return 0
    return -1 if n < 0 else 1

def find(l, element):
    try:
        return l.index(element)
    except ValueError:
        return -1

# mutates ft 
def follow(fl, ft):
    dr = fl[0] - ft[0]
    dc = fl[1] - ft[1]

    if abs(dr) <= 1 and abs(dc) <= 1:
        return

    ft[0] += sign(dr)
    ft[1] += sign(dc)

def format(lim, s):
    res = []
    for r in range(-lim, lim + 1):
        row = []
        for c in range(-lim, lim + 1):
            i = find(s, [r, c])
            if i == 0:
                row.append("H")
            elif i == len(s) - 1:
                row.append("T")
            elif i == -1:
                row.append(".")
            else:
                row.append(str(i))
        res.append("".join(row))
    return "\n".join(res)

def simulate(sr, sc, parts, lines):
    s = [[0, 0] for _ in range(parts)]
    used = {(0, 0)}
    for d, steps in lines:
        for _ in range(steps):
            update(d, s[0])
            for i in range(1, len(s)):
                follow(s[i - 1], s[i])
            used.add((s[-1][0], s[-1][1]))
    return len(used)

print(simulate(0, 0, 2, lines))
print(simulate(0, 0, 10, lines))
