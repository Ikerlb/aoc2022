from sys import stdin
import re
from collections import deque
from functools import reduce

lines = "".join(stdin)
descriptions = [g.splitlines() for g in lines.split("\n\n")]

def extract(l):
    return int(re.search(r"\d+", l).group())

class Monkey:
    @staticmethod
    def parse(s):
        items = deque(map(int, s[0].replace("  Starting items: ", "").split(", ")))
        limit = extract(s[2])
        op_s = "(" + s[1].replace("  Operation: new = ", "") + f")"
        operation = lambda old: eval(op_s, {"old": old})
        condition = lambda worry: extract(s[3]) if (worry % limit) == 0 else extract(s[4])
        inspections = 0
        return Monkey(items, operation, limit, condition, inspections)

    def __init__(self, items, operation, limit, condition, inspections):
        self.items = items
        self.operation = operation
        self.limit = limit
        self.condition = condition
        self.inspections = inspections

    def round(self, divide):
        yield from [self.step(divide) for _ in range(len(self.items))]

    def step(self, divide):
        item = self.items.popleft()
        worry = self.operation(item)
        if divide:
            worry //= 3
        self.inspections += 1
        #print("bonsaba", item, self.condition(worry), worry)
        return self.condition(worry), worry

    def add(self, item):
        self.items.append(item)

    def __repr__(self):
        return f'{",".join(map(str, self.items))}'

    def copy(self):
        return Monkey(self.items.copy(), self.operation, self.limit, self.condition, self.inspections)

monkeys = {extract(l[0]):Monkey.parse(l[1:]) for l in descriptions}

# mutates monkeys
def round(monkeys, divide, mult):
    for i, monkey in monkeys.items():
        for m, nw in monkey.round(divide):
            monkeys[m].add(nw % mult)

def rounds(monkeys, n, divide, m):
    for i in range(n):
        round(monkeys, divide, m)
    s = sorted(m.inspections for m in monkeys.values())
    return s[-1] * s[-2]

def prod(l):
    res = 1
    for n in l:
        res *= n
    return res

# calculate lcm
def lcm(a, b):
    return abs(a * b) // gcd(a, b)

# calculate gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

m = reduce(lcm, (m.limit for m in monkeys.values()))

# p1
print(rounds({k:v.copy() for k, v in monkeys.items()}, 20, True, m))

# p2
print(rounds({k:v.copy() for k, v in monkeys.items()}, 10000, False, m))
