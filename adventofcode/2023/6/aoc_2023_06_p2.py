import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class race:
    def __init__(self, time:int, distance:int):
        self.time = time
        self.distance = distance
        self.min_charge = 0
        self.max_charge = 0

    def __str__(self):
        return str(self.distance) + "mm@" + str(self.time) + "s - (" + str(self.min_charge) + " <= c <= " + str(self.max_charge) + ") - Diff: " + str(self.max_charge - self.min_charge)

lines = open("test_06.txt", "r").readlines()
races = []

time_match = re.search(r"Time:([0-9]+)", re.sub(r"\s*", "", lines[0]))
dist_match = re.search(r"Distance:([0-9]+)", re.sub(r"\s*", "", lines[1]))
races.append(race(int(time_match.group(1)), int(dist_match.group(1))))

ways = 0

for r in races:
    c = 0
    while c < r.time:
        # Iterate over the race for range(time)
        # Try to find min and max time for charging to achieve dist
        c += 1

        if (r.time - c) * c > r.distance:
            if r.min_charge == 0:
                r.min_charge = c
            
            r.max_charge = c
        else:
            if r.max_charge > 0:
                break
    
    # Part 1
    diff = (r.max_charge - r.min_charge + 1)

    if ways == 0:
        ways = diff
    else:
        ways *= diff
    
    print(r)

print("Part 1 Number of Ways: " + str(ways))