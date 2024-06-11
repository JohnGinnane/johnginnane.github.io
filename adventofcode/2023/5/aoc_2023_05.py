import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class map:
    def __init__(self, source_type, source_start, dest_type, dest_start, range):
        self.source_type = source_type
        self.source_start = source_start
        self.dest_type = dest_type
        self.dest_start = dest_start
        self.range = range

    def __str__(self):
        output = ""

        output += "FROM: " + pad(self.source_type, 12)
        output +=  " TO: " + pad(self.dest_type, 12)
        output += " SRC: " + pad(self.source_start, 4)
        output += " DST: " + pad(self.dest_start, 4)
        output += " RNG: " + pad(self.range, 4)

        return output

lines = open("test_05.txt", "r").readlines()
seeds = []
maps = []

mapping = False
map_from = ""
map_to = ""
map_destination = 0
map_source = 0
map_range = 0

for line in lines:
    if line.strip() == "":
        continue
    
    if not mapping:
        # Identify seeds
        seed_matches = re.findall(r"[0-9]+", line)
        for m in seed_matches:
            seeds.append(int(m))

        mapping = True
    else:
        # Do the rest of the code
        # If the first character is not a digit then assume new mapping
        map_match = re.match(r"([a-zA-Z]+)-to-([a-zA-Z]+) map:", line)
        
        if map_match:
            map_from = map_match.group(1)
            map_to = map_match.group(2)
        else:
            map_match = re.match(r"([0-9]+) ([0-9]+) ([0-9]+)", line)

            if map_match:
                map_destination = int(map_match.group(1))
                map_source = int(map_match.group(2))
                map_range = int(map_match.group(3))

                maps.append(map(map_from, map_source, map_to, map_destination, map_range))

print(seeds)

for m in maps:
    print(m)