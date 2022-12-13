from collections import deque
from sys import stdin

heightmap = [list(line[:-1]) for line in stdin]

def find(heightmap, ch):
    for r in range(len(heightmap)):
        for c in range(len(heightmap[0])):
            if heightmap[r][c] == ch:
                return r, c

def format(heightmap, used):
    res = []
    for r in range(len(heightmap)):
        row = []
        for c in range(len(heightmap[0])):
            if (r, c) in used:
                row.append(str(used[(r, c)]).rjust(2))
            else:
                row.append(heightmap[r][c].rjust(2))
        res.append(" ".join(row))
    return "\n".join(res)

# remove S from heightmap
def bfs(heightmap, start, end):
    er, ec = end
    steps = 0
    used = {(r, c):steps for r, c in start}
    q = deque(start)
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if r == er and c == ec:
                return steps
            for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nr, nc = r + dr, c + dc
                if not 0 <= nr < len(heightmap):
                    continue
                if not 0 <= nc < len(heightmap[0]):
                    continue
                #print(heightmap[r][c], heightmap[nr][nc], ord(heightmap[r][c]), ord(heightmap[nr][nc]))
                if (nr, nc) in used or ord(heightmap[r][c]) + 1 < ord(heightmap[nr][nc]):
                    continue
                used[(nr, nc)] = steps + 1
                q.append((nr, nc))
        steps += 1
    return None


start, end = find(heightmap, 'S'), find(heightmap, 'E')

heightmap[start[0]][start[1]] = 'a'
heightmap[end[0]][end[1]] = 'z'

# p1
print(bfs(heightmap, [start], end))

# p2
p2 = [(r, c) for r in range(len(heightmap)) for c in range(len(heightmap[0])) if heightmap[r][c] == 'a']
print(bfs(heightmap, p2, end))
