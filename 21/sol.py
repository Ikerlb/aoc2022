import fileinput
from collections import deque, defaultdict
from functools import lru_cache
from types import FunctionType

lines = [line.strip() for line in fileinput.input(encoding = 'utf-8')]

class Node:
    def __init__(self, val, left = None, right = None, expr = None): 
        self.val = val
        self.left = left
        self.right = right
        self.expr = expr

deps = defaultdict(list)
incoming = defaultdict(int)
vals = {}

for line in lines:
    monkey, rest = line.split(': ')
    if rest.isnumeric():
        vals[monkey] = int(rest)
        incoming[monkey] = 0
    else:
        m1, op, m2 = rest.split(' ')
        deps[m1].append(monkey)
        deps[m2].append(monkey)
        incoming[monkey] += 2
        vals[monkey] = (op, m1, m2)


def topo(deps, incoming):
    q = deque()
    for monkey in incoming:
        if incoming[monkey] == 0:
            q.append(monkey)
    while q:
        for _ in range(len(q)):
            monkey = q.popleft()
            yield monkey
            for dep in deps[monkey]:
                incoming[dep] -= 1
                if incoming[dep] == 0:
                    q.append(dep)

# create a single long expression
#def compile_expression(start, topo_sorted, vals, func_name):
#    s = start
#    for monkey in reversed(topo_sorted):
#        if monkey == "humn":
#            continue
#        elif type(vals[monkey]) is int:
#            s = s.replace(monkey, str(vals[monkey]))
#            continue
#        op, m1, m2 = vals[monkey]
#        if op == '+':
#            s = s.replace(monkey, f"({m1} + {m2})")
#        elif op == '*':
#            s = s.replace(monkey, f"({m1} * {m2})")
#        elif op == '/':
#            s = s.replace(monkey, f"({m1} // {m2})")
#        else:
#            s = s.replace(monkey, f"({m1} - {m2})")
#    comp_l = [
#        f"def {func_name}(humn):",
#        f"    return {s}"
#    ]
#    comp_s = "\n".join(comp_l)
#    comp = compile(comp_s, '<string>', 'exec')
#    return FunctionType(comp.co_consts[0], globals(), func_name)

def gen_tree(topo_sorted, vals):
    d = {}
    for monkey in topo_sorted:
        if monkey == "humn":
            node = Node(monkey, expr = "humn")
        elif type(vals[monkey]) is int:
            node = Node(vals[monkey], expr = f"{monkey} = {vals[monkey]}")
        else:
            op, m1, m2 = vals[monkey]
            node = Node(op, d[m1], d[m2], f"{monkey} = {m1} {op} {m2}")
        d[monkey] = node
    return d, node

def eval_tree(node):
    if node.left is None and node.right is None:
        return node.val
    op = node.val
    if op == '+':
        return eval_tree(node.left) + eval_tree(node.right)
    elif op == '*':
        return eval_tree(node.left) * eval_tree(node.right)
    elif op == '/':
        return eval_tree(node.left) // eval_tree(node.right)
    else:
        return eval_tree(node.left) - eval_tree(node.right)

def fmt(node):
    if node.left is None and node.right is None:
        return node.val
    else:
        return f"({fmt(node.left)} {node.val} {fmt(node.right)})"

@lru_cache(None)
def has_humn(node):
    if node.left is None and node.right is None:
        return node.val == "humn"
    return has_humn(node.left) or has_humn(node.right)

def inv(op):
    if op == "+":
        return "-"
    elif op == "*":
        return "/"
    elif op == "/":
        return "*"
    elif op == "-":
        return "+"

def ex(op, v1, v2):
    if op == "+":
        return v1 + v2
    elif op == "*":
        return v1 * v2
    elif op == "/":
        return v1 // v2
    elif op == "-":
        return v1 - v2

def regression(node, result):
    if node.val == "humn":
        return result
    if has_humn(node.left):
        other = eval_tree(node.right)
        r = regression(node.left, ex(inv(node.val), result, other))
    else:
        other = eval_tree(node.left)
        if node.val in "/-":
            r = regression(node.right, ex(node.val, other, result))
        else:
            r = regression(node.right, ex(inv(node.val), result, other))
    return r

topo_sorted = list(topo(deps, incoming))
d, root = gen_tree(topo_sorted, vals)

# p1
d["humn"].val = vals["humn"]
print(eval_tree(root))
d["humn"].val = "humn"

# p2
_, m1, m2 = vals["root"]
if has_humn(d[m1]):
    res = regression(d[m1], eval_tree(d[m2]))
else:
    res = regression(d[m2], eval_tree(d[m1]))
d["humn"].val = res
assert(eval_tree(d[m2]) == eval_tree(d[m1]))
print(res)
