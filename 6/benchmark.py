from collections import Counter
from sys import stdin
import timeit

signal = input()

s1 = f"""
from collections import Counter
signal = "{signal}"
def first_non_repeating_window(signal, size):
    w = Counter(signal[:size])
    if sum(1 for v in w.values() if v == 1) == size:
        return size - 1
    for i in range(size, len(signal)):
        w[signal[i - size]] -= 1

        w[signal[i]] += 1 
        if sum(1 for v in w.values() if v == 1) == size:
            return i
    return None

first_non_repeating_window(signal, 14)
"""

s2 = f"""
from collections import Counter
signal = "{signal}"
def first_non_repeating_window(signal, size):
    w = Counter(signal[:size])
    uniq = sum(1 for c, v in w.items() if v == 1)
    if uniq == size:
        return size - 1
    for i in range(size, len(signal)):
        if w[signal[i - size]] == 1:
            uniq -= 1
            del w[signal[i - size]]
        elif w[signal[i - size]] == 2:
            uniq += 1
            w[signal[i - size]] -= 1
        else:
            w[signal[i - size]] -= 1
        
        if w[signal[i]] == 0:
            uniq += 1
        elif w[signal[i]] == 1:
            uniq -= 1
        w[signal[i]] += 1

        if uniq == size:
            return i
    return None

first_non_repeating_window(signal, 14)
"""

print(timeit.timeit(s1, number = 10000))
print(timeit.timeit(s2, number = 10000))
