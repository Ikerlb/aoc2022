from sys import stdin

class World:
    def __init__(self, abyss = 0):
        self.particles = {}
        self.abyss = abyss
        
    def add_particule(self, particle):
        r, c = particle
        self.particles[(r, c)] = particle
        self.abyss = max(self.abyss, r + 1)

    def copy(self):
        w = World()
        w.particles = self.particles.copy()
        w.abyss = self.abyss
        return w

    def __repr__(self):
        mnr = min(self.particles.values(), key=lambda p: p.r).r
        mnc = min(self.particles.values(), key=lambda p: p.c).c

        mxr = max(self.particles.values(), key=lambda p: p.r).r
        mxc = max(self.particles.values(), key=lambda p: p.c).c
    
        res = []
        for r in range(mnr - 5, mxr + 5):
            row = []
            for c in range(mnc - 5, mxc + 5):
                if (r, c) in self.particles:
                    row.append(f"{self.particles[(r, c)]}")
                else:
                    row.append('.')
            res.append("".join(row))
        return "\n".join(res)

    # mutates p and adds to self
    def drop(self, p):
        r, c = p
        while r + 1 <= self.abyss and any((r + 1, c + dc) not in self.particles for dc in range(-1, 2)):
            if (r + 1, c) not in self.particles:
                r += 1
            elif (r + 1, c - 1) not in self.particles:
                r += 1
                c -= 1
            else:
                r += 1
                c += 1
        p.r = r
        p.c = c
        self.particles[(r, c)] = p
        return r + 1 <= self.abyss

class Particle:
    def __init__(self, r, c, t):
        self.r = r
        self.c = c
        self.t = t

    def __iter__(self):
        yield self.r
        yield self.c

    def __repr__(self):
        return f"{self.t}"

def parse(point):
    c, r = map(int, point.split(","))
    return r, c

def yield_path(s):
    points = s.split(" -> ")
    prev = parse(points[0])

    for point in map(parse, points[1:]):
        yield (prev, point)
        prev = point

def yield_rocks(p1, p2):
    r1, c1 = p1
    r2, c2 = p2

    if r1 == r2:
        for c in range(min(c1, c2), max(c1, c2) + 1):
            yield Particle(r1, c, "#")
    else:
        for r in range(min(r1, r2), max(r1, r2) + 1):
            yield Particle(r, c1, "#")

grid = World()


for line in stdin:
    for p1, p2 in yield_path(line[:-1]):
        for rock in yield_rocks(p1, p2):
            grid.add_particule(rock)

def part1(grid, sr, sc):
    i = 0
    while True:
        sand = Particle(sr, sc, "o")
        if not grid.drop(sand):
            break
        i += 1
    return i

def part2(grid, sr, sc):
    i = 0
    while True:
        sand = Particle(sr, sc, "o")
        grid.drop(sand)
        if sand.r == sr and sc == sand.c:
            break
        i += 1
    return i + 1

g1 = grid.copy()
print(part1(g1, 0, 500))

g2 = grid.copy()
print(part2(g2, 0, 500))
