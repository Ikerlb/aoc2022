from sys import stdin

rounds = []

for line in stdin:
    rounds.append(line[:-1].split(" "))

def part1(pred, resp):
    o_pred = ord(pred) - ord('A')  
    o_resp = ord(resp) - ord('X')
    if o_pred == o_resp:
        return 3 + o_resp + 1
    elif (o_pred + 1) % 3 == o_resp: 
        return 6 + o_resp + 1
    else:
        return 0 + o_resp + 1

def part2(pred, outcome):
    o_pred = ord(pred) - ord('A')
    if outcome == "X":
        return 0 + ((o_pred - 1) % 3) + 1
    elif outcome == "Y":
        return 3 + o_pred + 1
    else:
        return 6 + ((o_pred + 1) % 3) + 1

# p1
print(sum(part1(pred, resp) for pred, resp in rounds))

# p2
print(sum(part2(pred, outc) for pred, outc in rounds))
