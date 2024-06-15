import re
import math

def right(s, l):
    return str(s)[-l:]

def left(s, l):
    return str(s)[:l]

def pad(s, l):
    return right(" " * l + str(s), l)

def padr(s, l):
    return left(str(s) + " " * l, l)

class race:
    def __init__(self, time:int, distance:int):
        self.time = time
        self.distance = distance
        self.min_charge = 0
        self.max_charge = 0

    def __str__(self):
        return str(self.distance) + "mm@" + str(self.time) + "s - (" + str(self.min_charge) + " <= c <= " + str(self.max_charge) + ") - Diff: " + str(self.max_charge - self.min_charge)

lines = open("input_06.txt", "r").readlines()

time_match = re.search(r"Time:([0-9]+)", re.sub(r"\s*", "", lines[0]))
dist_match = re.search(r"Distance:([0-9]+)", re.sub(r"\s*", "", lines[1]))
big_race = race(int(time_match.group(1)), int(dist_match.group(1)))

# Distance = (MaxTime - ChargeTime) * ChargeTime
def findLimit(max:int, target:int):
    low = 0
    high = max
    mid = (high + low) // 2
    lower_limit = 0
    upper_limit = 0
    findUpper = False

    while True:
        dist = (max - mid) * mid

        if not findUpper:
            if dist < target:
                # Not charged for long enough
                # Look right
                low = mid
            else:
                # Charged for adequate amount of time, 
                # make note of this time (to find upper limit)
                # Look left (to find lower limit)
                lower_limit = mid
                high = mid
        else:
            if dist >= target:
                # Charged for long enough
                low = mid
                upper_limit = mid
            else:
                high = mid

        # Update mid to new location
        mid = (high + low) // 2

        if mid <= low and not findUpper:
            print("Finished lower limit, moving to upper")
            # Swap to finding upper limit
            findUpper = True
            low = 0
            high = max
            mid = (high + low) // 2
        elif high - low <= 1 and findUpper:
            print("Finished upper limit, exiting")
            # Finished binary search
            break

    return lower_limit, upper_limit

big_race.min_charge, big_race.max_charge = findLimit(big_race.time, big_race.distance)

print(big_race)
print("Part 2 Number of Ways: " + str(big_race.max_charge - big_race.min_charge + 1))