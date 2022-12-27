import fileinput

class GasStream:
    def __init__(self, pattern):
        self.i = 0
        self.pattern = pattern

    def __next__(self):
        res = self.pattern[self.i]
        self.i = (self.i + 1) % len(self.pattern)
        return res

def yield_infinitely(l):
    i = 0
    while True:
        yield l[i % len(l)]
        i += 1

class Rock:
    def __init__(self, lines, rep):
        self.lines = lines
        self.rep = rep
        self.cmin = min(i for i in range(len(lines)) if "#" in lines[i])
        self.cmax = max(i for i in range(len(lines)) if "#" in lines[i])
        self.rmin = min(i for row in lines for i in range(len(row)) if row[i] == "#")
        self.rmax = max(i for row in lines for i in range(len(row)) if row[i] == "#")

    def stuck(self, r, c, grid):
        for ri, ci in self:
            if grid.is_blocked(r+ri, c+ci):
                return True
        return False

    def __iter__(self):
        for ri in range(len(self.lines)):
            for ci in range(len(self.lines[0])):
                if self.lines[ri][ci] == "#":
                    yield -ri, ci

    def __repr__(self):
        return self.rep

def format(grid, rock, r, c):
    rcells = {(r+ri, c+ci) for ri, ci in rock}
    res = ["".join(["+"] + ["-" * (grid.width)] + ["+"])]
    for r in range(grid.highest + 1 + 6):
        row = ["|"]
        for c in range(0, grid.width):
            if (r, c) in grid.blocked:
                row.append(str(grid.blocked[r, c]))
            elif (r, c) in rcells:
                row.append("@")
            else:
                row.append(".")
        row.append("|")
        res.append("".join(row))
    return "\n".join(reversed(res))

class Grid:
    def __init__(self, width, blocked, highest):
        self.width = width
        self.blocked = blocked
        self.highest = highest

    def add(self, rock, gas, debug = False):
        cs = 2
        rs = self.highest + 4 + (len(rock.lines) - 1)
        r, c = rs, cs
        while True:
            s = next(gas)
            dc = 1 if s == ">" else -1

            if not rock.stuck(r, c + dc, self):
                c += dc

            if rock.stuck(r - 1, c, self):
                break
            else:
                r -= 1

        relative_row = self.highest - r
        for dr, dc in rock:
            self.blocked[r + dr, c + dc] = rock
            self.highest = max(self.highest, r + dr)

        return gas.i, relative_row, c

    def add_bulk(self, rocks, gas, debug = False):
        return [self.add(rock, gas, debug) for rock in rocks]

    def copy(self):
        d = {k:v for k, v in self.blocked.items()}
        return Grid(self.width, d, self.highest)

    def is_blocked(self, r, c):
        return (r, c) in self.blocked or r < 0 or c < 0 or c >= self.width

    def __repr__(self):
        res = ["".join(["+"] + ["-" * self.width] + ["+"])]
        for r in range(self.highest + 1 + 6):
            row = ["|"]
            for c in range(0, self.width):
                if (r, c) in self.blocked:
                    row.append(str(self.blocked[r, c]))
                else:
                    row.append(".")
            row.append("|")
            res.append("".join(row))
        return "\n".join(res)

gas = "".join(line[:-1] for line in fileinput.input(encoding="utf-8"))

rocks = []

rocks.append(Rock(["####"], "1"))
rocks.append(Rock([
    ".#.",
    "###",   
    ".#."
], "2"))
rocks.append(Rock([
    "..#",
    "..#",
    "###",
], "3"))
rocks.append(Rock([
    "#",
    "#",
    "#",
    "#"
], "4"))
rocks.append(Rock([
    "##",
    "##"
], "5"))

grid = Grid(7, {}, -1)

def part1(grid, rocks, steps, gas):
    gas = GasStream(gas)
    for i, rock in zip(range(steps), yield_infinitely(rocks)):
        grid.add(rock, gas)
    return grid.highest + 1

def part2(grid, rocks, gas, limit):
    gas = GasStream(gas)
    seen = {}
    i = 0
    while (t := tuple(grid.add_bulk(rocks, gas))) not in seen:
        i += len(rocks)
        seen[t] = (i, grid.highest, gas.i)
    i += len(rocks)
    ph = grid.highest
    diff_height = ph - seen[t][1]
    diff_i = i  - seen[t][0]
    limit -= seen[t][0]
    h = seen[t][1]
    d, m = divmod(limit, diff_i)
    h += d * diff_height
    for _,rock in zip(range(m), yield_infinitely(rocks)):
        grid.add(rock, gas)
    return h + (grid.highest - ph) + 1

print(part1(grid.copy(), rocks, 2022, gas))
print(part2(grid.copy(), rocks + rocks, gas, 1000000000000))
