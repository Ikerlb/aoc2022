from sys import stdin

def find_incorrect(s):
    m = len(s) >> 1
    l, r = set(s[:m]), set(s[m:])
    return (l & r).pop()

def priority(c):
    if c.isupper():
        return ord(c) - ord('A') + 27 
    else:
        return ord(c) - ord('a') + 1

def find_badge(a, b, c):
    sa, sb, sc = set(a), set(b), set(c)
    return (sa & sb & sc).pop()

def chunks(s, cs):
    for i in range(0, len(s), cs):
        yield s[i:i + cs]

rucksacks = [l[:-1] for l in stdin]

# p1
print(sum(priority(find_incorrect(s)) for s in rucksacks))

# p2
print(sum(priority(find_badge(*c)) for c in chunks(rucksacks, 3)))
