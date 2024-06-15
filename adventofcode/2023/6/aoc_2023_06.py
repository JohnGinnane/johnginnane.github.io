import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class race:
    def __init__(self, time:float, distance:float):
        self.time = time
        self.distance = distance

    def __str__(self):
        return str(self.distance) + "mm@" + str(self.time) + "s" 

lines = open("test_05.txt", "r").readlines()
races = []

time_matches = re.findall(r"([0-9]+)+", lines[0])
dist_matches = re.findall(r"([0-9]+)+", lines[1])

for k in range(len(time_matches)):
    t = time_matches[k]
    d = dist_matches[k]
    races.append(race(t, d))

for r in races:
    print(r)