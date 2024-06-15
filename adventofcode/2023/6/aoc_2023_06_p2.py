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

time_match = re.search(r"Time:([0-9]+)", re.sub(r"\s*", "", lines[0]))
dist_match = re.search(r"Distance:([0-9]+)", re.sub(r"\s*", "", lines[1]))
big_race = race(int(time_match.group(1)), int(dist_match.group(1)))

ways = 0

# Distance = (MaxTime - ChargeTime) * ChargeTime
low = 0
high = big_race.time
mid = (high + low) // 2
i = 0

def findLowerLimit(max:int):
    low = 0
    high = max
    mid = (high + low) // 2
    i = 0
    lower_limit = 0

    while mid > low:
        dist = (max - mid) * mid
        debug = pad(i, 4) + ": "
        debug += str(low) + "-" + str(mid) + "-" + str(high)

        if dist < big_race.distance:
            # Not charged for long enough
            # Look right
            low = mid
            debug += pad("looking right", 20)
        else:
            # Charged for adequate amount of time, 
            # make note of this time (to find upper limit)
            # Look left (to find lower limit)
            lower_limit = mid
            high = mid
            debug += pad("looking left", 20)

        mid = (high + low) // 2
        debug += " " + str(lower_limit)
        print(debug)
        i+=1

        # watchdog
        if i >= 20:
            print("Too many steps, stopping!")
            break

    return lower_limit

big_race.min_charge = findLowerLimit(big_race.time)

print(big_race)
print("Part 2 Number of Ways: " + str(ways))