from collections import Counter
from sys import stdin

signal = input()

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

# p1
print(first_non_repeating_window(signal, 4) + 1)

# p2
print(first_non_repeating_window(signal, 14) + 1)

