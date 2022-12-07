from sys import stdin
import math
import re

cmds = [line[:-1] for line in stdin]

class Node:
    def __init__(self, name, file_weight = None):
        self.name = name
        self.children = {}
        self.file_weight = file_weight

    def __contains__(self, item):
        return item in self.children

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children[key]

    def __iter__(self):
        yield from self.children.values()

    def __bool__(self):
        return bool(self.children)

    def create_directory(self, d):
        if d not in self:
            self[d] = Node(d)
        return self[d]

    def create_file(self, name, weight):
        if name not in self:
            self[name] = Node(name, file_weight = weight)
        return self[name]

def walk(cmds):
    root = Node("/")
    dirs = [root]
    i = 0
    while i < len(cmds):
        cmd = cmds[i]
        if cmd == "$ cd /":
            dirs = [root]
        elif cmd == "$ cd ..":
            dirs.pop()
        elif (m := re.match(r"\$ cd (.+)", cmd)) is not None:
            (d, ) = m.groups()
            nd = dirs[-1].create_directory(d)
            dirs.append(nd)
        elif cmd == "$ ls":
            while i + 1 < len(cmds) and cmds[i + 1][0] != "$":
                i += 1
                fst, snd = cmds[i].split(" ")
                if fst == "dir":
                    dirs[-1].create_directory(snd)
                else:
                    dirs[-1].create_file(snd, int(fst))
        i += 1
    return root

def pretty_print(node, s = 1):
    if not node:
        return f"{node.name} ({node.file_weight})"
    rest =  "\n".join((" " * s) + pretty_print(nn, s + 1) for nn in node)
    return node.name + "\n" + rest

tree = walk(cmds)

def dfs(node, limit):
    if not node:
        return 0, node.file_weight
    ts = s = 0
    for nn in node:
        nnt, nns = dfs(nn, limit)
        ts += nnt
        s += nns
    return (0 if s > limit else s) + ts, s

def size(node):
    if not node:
        return node.file_weight
    return sum(size(nn) for nn in node)

def dfs2(node, limit):
    if not node:
        return math.inf, node.file_weight
    tm, s = math.inf, 0
    for nn in node:
        nnm, nns = dfs2(nn, limit)
        tm = min(nnm, tm)
        s += nns
    return min(tm, s) if s >= limit else tm, s 

# p1
print(dfs(tree, 100000)[0])

# p2
available = 70000000 - size(tree)
remaining = 30000000 - available
print(dfs2(tree, remaining)[0])
