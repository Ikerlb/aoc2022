import fileinput
from collections import deque

enc = [int(x) for x in fileinput.input(encoding = "utf-8")]

def mod(x, b):
    return x - int(x / b) * b

# 1 <-> 2 <-> -3 <-> 3 <-> -2 <-> 0 <-> 4|-

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def walk(self, k):
        #print(self.val, k)
        node = self
        if k < 0:
            for _ in range(-k):
                node = node.left
            return node
        else:
            for _ in range(k):
                node = node.right
            return node

    # make self's next node
    # the one passed as param
    def change_next(self, node):
        self.right.left = node
        node.right = self.right
        node.left = self
        self.right = node

    # make self's prev node
    # the one passed as param
    def change_prev(self, node):
        self.left.right = node
        node.left = self.left
        node.right = self
        self.left = node

    # soft deletes this node
    def remove(self):
        self.left.right = self.right
        self.right.left = self.left
        self.left = self.right = None

    def __repr__(self):
        return f"{self.val}"

class CircularList:
    def __init__(self, vals):
        self.head = None
        self.tail = None
        self.zero = None
        self.size = 0

        for v in vals:
            node = self._add(v)
            if v == 0:
                self.zero = node
            self.size += 1

        self.tail.right = self.head
        self.head.left = self.tail

    # adds to the tail, internal use only
    def _add(self, val):
        node = Node(val)
        if self.head is None and self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.right = node
            node.left = self.tail
            self.tail = node
        return node

    # 4, 5, 6, 1, 7, 8, 9
    # 4, 5, 6, _, 7, 8, 9
    def mix(self, order):
        for node in order:        
            k = mod(node.val, self.size - 1)
            if k == 0:
                continue
            n_left, n_right = node.left, node.right
            node.remove()
            dummy = Node("__dummy__", left=n_left, right=n_right)
            target = dummy.walk(k)
            if k < 0:
                target.change_prev(node)
            else:
                target.change_next(node)

    def details(self):
        res = []
        for node in self.iter(self.head):
            res.append(f"{node=}, {node.left=}, {node.right=}")
        return "\n".join(res)

    def find(self, k):
        n = self.zero
        return n.walk(k).val

    def iter(self, start):
        st = set()
        node = start
        while node not in st:
            yield node
            st.add(node)
            node = node.right

    def __repr__(self):
        return " -> ".join(map(str, self.iter(self.head))) + " -||"

def mix_and_find(cl, order):
    cl.mix(order)
    return cl.find(1000) + cl.find(2000) + cl.find(3000)

# p1
cl = CircularList(enc)
order = list(cl.iter(cl.head))
print(mix_and_find(cl, order))

# p2
cl = CircularList([e * 811589153 for e in enc])
order = list(cl.iter(cl.head))
print(mix_and_find(cl, list(order * 10)))


