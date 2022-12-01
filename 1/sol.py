from sys import stdin

text = "".join(stdin)
groups = [sum(map(int, g.splitlines())) for g in text.split("\n\n")]

groups.sort()

# part1
print(groups[-1])

# part2
print(sum(groups[-3:]))
