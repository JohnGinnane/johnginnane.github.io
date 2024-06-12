import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class number_range:
    def __init__(self, start:int, length:int):
        self.start = start
        self.length = length

        if self.length < 0:
            self.length *= -1
        
        self.end = self.start + self.length

    def __str__(self):
        p = 3
        return pad(self.start, p) + "..." + pad(self.end, p)

class map_range:
    def __init__(self, source_start:int, destination_start:int, length:int):
        map_range(number_range(source_start, length), number_range(destination_start, length))

    def __init__(self, source_range:number_range, destination_range:number_range):
        self.source_range = source_range
        self.destination_range = destination_range
    
    def __str__(self):
        return str(self.source_range) + " -> " + str(self.destination_range)

class map:
    def __init__(self, source_type, dest_type):
        self.source_type = source_type
        self.destination_type = dest_type
        self.ranges = []

    def getDestination(self, source:int):
        for r in self.ranges:            
            if source >= r.source_range.start and source <= r.source_range.end:
                return source + (r.destination_range.start - r.source_range.start)
            
        return source

    def addMapRange(self, source_range:number_range, destination_range:number_range):
        # Keep ranges in order pls
        for r in self.ranges:
            if source_range.start == r.source_range.start and destination_range.start == r.destination_range.start:
                return
        
        new_map_range = map_range(source_range, destination_range)

        # No recorded ranges, just slap it in
        if len(self.ranges) <= 0:
            self.ranges.append(new_map_range)
        else:
            # Try to place in order
            found = False
            for k in range(len(self.ranges)):
                r = self.ranges[k]
                if r.source_range.start > new_map_range.source_range.start:
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
            output += "\n\t" + str(r)

        return output

def getMap(source_type, destination_type):
    for m in maps:
        if m.source_type == source_type and m.destination_type == destination_type:
            return m

    return None

#lines = open("input_05.txt", "r").readlines()
lines = open("test_05.txt", "r").readlines()
seeds = []
seed_ranges = []
maps = []

mapping = False
last_map_index = -1

for line in lines:
    if line.strip() == "":
        continue
    
    if not mapping:
        # Part 1 - Identify seeds
        seed_matches = re.findall(r"[0-9]+", line)
        for m in seed_matches:
            seeds.append(int(m))

        # Part 2 - Seed Ranges
        seed_matches = re.findall(r"([0-9]+) ([0-9]+)", line)
        
        for pairs in seed_matches:
            #print(pairs[0] + " ... " + str(int(pairs[0]) + int(pairs[1])))
            seed_ranges.append(number_range(int(pairs[0]), int(pairs[1])))

        mapping = True
    else:
        # Read the rest of the file
        # If the first character is not a digit then assume new mapping
        map_match = re.match(r"([a-zA-Z]+)-to-([a-zA-Z]+) map:", line)
        
        if map_match:
            last_map_index = -1
            source = map_match.group(1)
            destination = map_match.group(2)

            # Try to find existing mapping
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

                destination_start = int(map_match.group(1))
                source_start = int(map_match.group(2))
                length = int(map_match.group(3)) - 1

                last_map.addMapRange(number_range(source_start, length), number_range(destination_start, length))

# for m in maps:
#     print(m)

path = {"seed":        "soil",
        "soil":        "fertilizer",
        "fertilizer":  "water",
        "water":       "light",
        "light":       "temperature",
        "temperature": "humidity",
        "humidity":    "location"}

# lowest_location = -1

# for n in seeds:
#     last_number = n
#     output = next(iter(path)) + " " + str(last_number)

#     for from_type in path:
#         to_type = path[from_type]
#         last_number = getMap(from_type, to_type).getDestination(last_number)
#         output += ", " + to_type + " " + str(last_number)

#         if from_type == list(path)[-1]:
#             if lowest_location < 0 or last_number < lowest_location:
#                 lowest_location = last_number
    
#     #print(output)

# print("\nPart 1 Lowest Location: " + str(lowest_location) + "\n\n")

# print("Part 2 Seed Ranges:")
# for r in seed_ranges:
#     print(r)

def filterRange(r:number_range, m:map):
    if m == None:
        return [r]
    
    if m.ranges == None:
        return [r]
    
    if len(m.ranges) <= 0:
        return [r]
    
    output = []

    # r     {79...93}
    # mr[1] {50...97} -> {52...99}
    # mr[2] {98...99} -> {50...51}

    rangeConsumed = False
    for mr in m.ranges:
        print("Range: " + str(r))
        print("Check: " + str(mr))

        # If the entire input range is inside the map range
        # then just convert to destination
        if r.start >= mr.source_range.start and r.end <= mr.source_range.end:
            output.append(number_range(m.getDestination(r.start), r.length))
            rangeConsumed = True
            break
        elif r.start >= mr.source_range.start and r.start <= mr.source_range.end:
            sub_start = m.getDestination(r.start)
            sub_end = m.getDestination(mr.source_range.end)
            sub_range = number_range(sub_start, sub_end - sub_start)
            output.append(sub_range)

            # Truncate the input range for future checks
            r.start = mr.source_range.end + 1

        elif r.end >= mr.source_range.start and r.end <= mr.source_range.end:
            # End of input range fits into map range
            # so cut into two pieces and finish
            sub_start_1 = r.start
            sub_end_1 = mr.source_range.start - 1
            sub_range_1 = number_range(sub_start_1, sub_end_1 - sub_start_1)
            output.append(sub_range_1)

            sub_start_2 = m.getDestination(mr.source_range.start)
            sub_end_2 = m.getDestination(r.end)
            sub_range_2 = number_range(sub_start_2, sub_end_2 - sub_start_2)
            output.append(sub_range_2)
            return output
    
    # Range (or what's left of it) couldn't
    # fit into map range
    if not rangeConsumed:
        output.append(r)

    return output

TestMap = None
TestSeedRange = seed_ranges[1]
for m in maps:
    if m.source_type == "light" and m.destination_type == "temperature":
        TestMap = m
        break

if TestMap:
    print("Testing seed range" + str(TestSeedRange))
    print(TestMap)

    result = filterRange(seed_ranges[1], TestMap)
    for huh in result:
        print(huh)