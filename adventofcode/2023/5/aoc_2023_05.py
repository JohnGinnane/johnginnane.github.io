import re
import time

solution_start = time.time()
def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class number_range:
    def __init__(self, start:int, end:int):
        # if start > end:
        #     temp = start
        #     start = end
        #     end = temp
        
        self.start = start
        self.end = end

    def __str__(self):
        p = 3
        return pad(self.start, p) + "..." + pad(self.end, p)

class map_range:
    def __init__(self, source_start:int, destination_start:int, length:int):
        map_range(number_range(source_start, source_start + length), number_range(destination_start, destination_start + length))

    def __init__(self, source_range:number_range, destination_range:number_range):
        self.source_range = source_range
        self.destination_range = destination_range
    
    def __str__(self):
        return str(self.source_range) + " -> " + str(self.destination_range) + " (" + pad(self.destination_range.start - self.source_range.start, 3) + ")"

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

    def addMapRange(self, source_start:int, destination_start:int, length:int):
        source_range = number_range(source_start, source_start + length)
        destination_range = number_range(destination_start, destination_start + length)

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

lines = open("input_05.txt", "r").readlines()
#lines = open("test_05.txt", "r").readlines()
seeds = []
seed_ranges = []
maps = []

mapping = False
last_map_index = -1

# Interpret mapping data
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
            seed_start = int(pairs[0])
            seed_length = int(pairs[1])
            # 50...54 = 5 (50, 51, 52, 53, 54)

            seed_end = seed_start + seed_length - 1

            #print(pairs[0] + " ... " + str(int(pairs[0]) + int(pairs[1])))
            seed_ranges.append(number_range(seed_start, seed_end))

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

                last_map.addMapRange(source_start, destination_start, length)

path = {"seed":        "soil",
        "soil":        "fertilizer",
        "fertilizer":  "water",
        "water":       "light",
        "light":       "temperature",
        "temperature": "humidity",
        "humidity":    "location"}

lowest_location = -1

for n in seeds:
    last_number = n
    #output = next(iter(path)) + " " + str(last_number)

    for from_type in path:
        to_type = path[from_type]
        last_number = getMap(from_type, to_type).getDestination(last_number)
        #output += ", " + to_type + " " + str(last_number)

        if from_type == list(path)[-1]:
            if lowest_location < 0 or last_number < lowest_location:
                lowest_location = last_number
    
    #print(output)

print("\nPart 1 Lowest Location: " + str(lowest_location) + "\n\n")
part_1_end = time.time()

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
        # print("Range: " + str(r))
        # print("Check: " + str(mr))

        # If the entire input range is inside the map range
        # then just convert to destination
        if r.start >= mr.source_range.start and r.end <= mr.source_range.end:
            output.append(number_range(m.getDestination(r.start), m.getDestination(r.end)))
            rangeConsumed = True
            break
        elif r.start >= mr.source_range.start and r.start <= mr.source_range.end:
            sub_start = m.getDestination(r.start)
            sub_end = m.getDestination(mr.source_range.end)
            sub_range = number_range(sub_start, sub_end)
            output.append(sub_range)

            # Truncate the input range for future checks
            r.start = mr.source_range.end + 1

        elif r.end >= mr.source_range.start and r.end <= mr.source_range.end:
            # End of input range fits into map range
            # so cut into two pieces and finish
            sub_start_1 = r.start
            sub_end_1 = mr.source_range.start - 1
            sub_range_1 = number_range(sub_start_1, sub_end_1)
            output.append(sub_range_1)

            sub_start_2 = m.getDestination(mr.source_range.start)
            sub_end_2 = m.getDestination(r.end)
            sub_range_2 = number_range(sub_start_2, sub_end_2)
            output.append(sub_range_2)
            return output
    
    # Range (or what's left of it) couldn't
    # fit into map range
    if not rangeConsumed:
        output.append(r)

    return output

def printListOfNumberRanges(ranges):
    output = ""
    for r in ranges:
        if output != "":
            output += ", "
        output += "'" + str(r) + "'"

    print("[" + output + "]")

def numberRangeKey(e):
    return e.start

cur_ranges = seed_ranges.copy()
cur_ranges.sort(key=numberRangeKey)
#printListOfNumberRanges(cur_ranges)

for from_type in path:
    to_type = path[from_type]
    cur_map = getMap(from_type, to_type)
    new_ranges = []

    #print("\t" + str(cur_map))
    while len(cur_ranges) > 0:
        new_ranges = new_ranges + filterRange(cur_ranges[0], cur_map)
        del cur_ranges[0]
    
    new_ranges.sort(key=numberRangeKey)
    #printListOfNumberRanges(new_ranges)
    cur_ranges = new_ranges.copy()

print("\n Part 2 Lowest Location: " + str(cur_ranges[0].start))
part_2_end = time.time()

print("Part 1: " + str((part_1_end - solution_start) * 1000) + "ms")
print("Part 2: " + str((part_2_end - solution_start) * 1000) + "ms")