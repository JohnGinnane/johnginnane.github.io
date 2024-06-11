import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class map_range:
    def __init__(self, source_start, dest_start, range):
        self.source_start = source_start
        self.dest_start = dest_start
        self.range = range

    def __str__(self):
        output  = "\n" + pad(self.source_start, 5) + " -> " + pad(self.dest_start, 5) + " ... " + pad(self.source_start + self.range, 5) + " -> " + pad(self.dest_start + self.range, 5)
        return output

class map:
    def __init__(self, source_type, dest_type):
        self.source_type = source_type
        self.destination_type = dest_type
        self.ranges = []

    def addMapRange(self, source_start, dest_start, new_range):
        # Keep ranges in order pls
        found = False
        for r in self.ranges:
            if source_start == r.source_start:
                found = True
                break

        if not found:
            new_map_range = map_range(source_start, dest_start, new_range)
            
            # No recorded ranges, just slap it in
            if len(self.ranges) <= 0:
                self.ranges.append(new_map_range)
            else:
                # Try to place in order
                found = False
                for k in range(len(self.ranges)):
                    v = self.ranges[k]
                    if v.source_start > source_start:
                        found = True
                        self.ranges.insert(k, new_map_range)
                        break

                # None found, just slap it in
                if not found:
                    self.ranges.append(new_map_range)

    def __str__(self):
        output = ""

        output += "FROM: " + pad(self.source_type, 12)
        output +=  " TO: " + pad(self.destination_type, 12)

        for r in self.ranges:
            output += "\t" + str(r)

        return output

lines = open("test_05.txt", "r").readlines()
seeds = []
maps = []

for k in range(3):
    print(k)

mapping = False
last_map_index = -1

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
            last_map_index = -1
            source = map_match.group(1)
            destination = map_match.group(2)

            # find the match
            for k in range(len(maps)):
                v = maps[k]
                if v.source_type == source and v.dest_type == destination:
                    last_map_index = k
                    break

            # Couldn't find mapping, create a new one
            if last_map_index < 0:
                newmap = map(source, destination)
                maps.append(newmap)
                last_map_index = len(maps) - 1
                #print("Creating a new map for " + str(newmap) + " at index " + str(last_map_index))
        else:
            map_match = re.match(r"([0-9]+) ([0-9]+) ([0-9]+)", line)
            
            if last_map_index >= 0 and last_map_index < len(maps) and map_match:
                last_map = maps[last_map_index]

                new_destination_start = int(map_match.group(1))
                new_source_start = int(map_match.group(2))
                new_range = int(map_match.group(3)) - 1

                last_map.addMapRange(new_source_start, new_destination_start, new_range)

print(seeds)

for m in maps:
    print(m)