from sys import stdin
import re
from collections import deque

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
        #print(f"taking {item=}, becomes {worry=} and then {res=}, passing to {self.condition(worry)}")
        self.inspections += 1
        print("bonsaba", item, self.condition(worry), worry)
        return self.condition(worry), worry

    def add(self, item):
        self.items.append(item % self.limit)

    def __repr__(self):
        return f'{",".join(map(str, self.items))}'

    def copy(self):
        return Monkey(self.items.copy(), self.operation, self.limit, self.condition, self.inspections)

monkeys = {extract(l[0]):Monkey.parse(l[1:]) for l in descriptions}

# mutates monkeys
def round(monkeys, divide):
    for i, monkey in monkeys.items():
        print(f"@ monkey {i}")
        for m, nw in monkey.round(divide):
            print("bonsaka", m, nw)
            monkeys[m].add(nw)

def rounds(monkeys, n, divide):
    print(f"starting with {monkeys}")
    for i in range(n):
        round(monkeys, divide)
        print(f"after {i} {monkeys}", [m.inspections for m in monkeys.values()])
    return monkeys

# p1
#m = rounds({k:v.copy() for k, v in monkeys.items()}, 20, True)
#s = sorted(m.inspections for m in m.values())
#print(s)
#print(s[-1] * s[-2])


# p2
monkeys = {k:v.copy() for k, v in monkeys.items()}
rounds(monkeys, 20, False)
print(monkeys)
print(list(m.inspections for m in monkeys.values()))

