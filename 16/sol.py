import fileinput
from collections import deque
from functools import lru_cache
from itertools import product

def parse_valve(line):
    words = line.split()
    valve_name = words[1]
    flow_rate = int(words[4].split('=')[1][:-1])
    leads_to = list(w.replace(",", "") for w in words[9:])
    return valve_name, flow_rate, leads_to

d, w = {}, {}

for line in fileinput.input(encoding="utf-8"):
    valve_name, flow_rate, leads_to = parse_valve(line)
    w[valve_name] = flow_rate
    d[valve_name] = leads_to

@lru_cache(None)
def dp(n, o, t, e):
    if t <= 0:
        return 0 if e == 0 else dp("AA", o, 26, e - 1)
    res = 0
    bs = 1 << v2i[n]
    if (bs & o) == 0 and w[n] > 0:
        res = max(res, dp(n, bs | o, t - 1, e) + (w[n] * (t - 1)))

    for nn in d[n]:
        res = max(res, dp(nn, o, t - 1, e))
    return res

v2i = {v:i for i, v in enumerate(d.keys())}
print(dp("AA", 0, 30, 0))
print(dp("AA", 0, 26, 1))
