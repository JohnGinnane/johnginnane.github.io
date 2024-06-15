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

lines = open("test_06.txt", "r").readlines()

time_match = re.search(r"Time:([0-9]+)", re.sub(r"\s*", "", lines[0]))
dist_match = re.search(r"Distance:([0-9]+)", re.sub(r"\s*", "", lines[1]))
big_race = race(int(time_match.group(1)), int(dist_match.group(1)))

# Distance = (MaxTime - ChargeTime) * ChargeTime
low = 0
high = big_race.time
mid = (high + low) // 2
i = 0

def findLimit(max:int, target:int, findUpper:bool):
    low = 0
    high = max
    mid = (high + low) // 2
    i = 0
    limit = 0

    while True:
        dist = (max - mid) * mid
        debug = pad(i, 4) + ": "
        debug += str(low) + "-" + str(mid) + "-" + str(high)

        if not findUpper:
            if dist < target:
                # Not charged for long enough
                # Look right
                low = mid
                debug = padr(debug, 30) + "looking right"
            else:
                # Charged for adequate amount of time, 
                # make note of this time (to find upper limit)
                # Look left (to find lower limit)
                limit = mid
                high = mid
                debug = padr(debug, 30) + "looking left "
        else:
            if dist >= target:
                # Charged for long enough
                low = mid
                limit = mid
                debug = padr(debug, 30) + "looking right"
            else:
                high = mid
                debug = padr(debug, 30) + "looking left "

        # Update mid to new location
        mid = (high + low) // 2

        debug += " " + pad(limit, 6)
        print(debug)

        if mid <= low or mid >= high:
            print("binary search complete")
            break
        i+=1

        # watchdog
        if i >= 20:
            print("Too many steps, stopping!")
            break

    return limit

big_race.min_charge = findLimit(big_race.time, big_race.distance, False)
big_race.max_charge = findLimit(big_race.time, big_race.distance, True)

print(big_race)
print("Part 2 Number of Ways: " + str(big_race.max_charge - big_race.min_charge + 1))