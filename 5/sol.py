from sys import stdin
from collections import defaultdict
import re

lines = "\n".join(line[:-1] for line in stdin)
fst, snd = lines.split("\n\n")

def parse_state(s):
    lines = s.splitlines()

    stacks = defaultdict(list)
    idx = {c:i for i, c in enumerate(lines.pop()) if c.isdigit()}
    while lines:
        line = lines.pop()
        for s, i in idx.items():
            if line[i] != " ":
                stacks[s].append(line[i])

    return stacks

def parse_moves(s):
    res = []
    for line in s.splitlines():
        k, src, dst = re.findall(r"\d+", line)
        res.append((int(k), src, dst))
    return res

state = parse_state(fst)
moves = parse_moves(snd)

# mutates state
def step(state, k, src, dst, preserve):
    inter = [state[src].pop() for _ in range(k)]
    if preserve:
        inter.reverse()
    state[dst].extend(inter)
    return state

def steps(state, moves, preserve = False):
    state = {k:state[k][:] for k in state}
    for k, src, dst in moves:
        step(state, k, src, dst, preserve)
    return state

def format(state):
    return "".join(state[k][-1] for k in sorted(state))
    
# p1
print(format(steps(state, moves)))

# p2
print(format(steps(state, moves, preserve = True)))
