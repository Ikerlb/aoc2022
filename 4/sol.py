from sys import stdin
from dataclasses import dataclass

@dataclass
class Interval:
    start: int 
    end: int 

    # other is contained in self
    def contains(self, other):
        return self.start <= other.start and other.end <= self.end 

    def overlaps(self, other):
        return self.start <= other.start <= self.end

def parse(line):
    fst, snd = line.split(",")
    fs, fe = map(int, fst.split("-"))
    ss, se = map(int, snd.split("-"))
    return Interval(fs, fe), Interval(ss, se)

pairs = [parse(line[:-1]) for line in stdin]

# p1
print(sum(1 for i1, i2 in pairs if i1.contains(i2) or i2.contains(i1)))

# p2
print(sum(1 for i1, i2 in pairs if i1.overlaps(i2) or i2.overlaps(i1)))
