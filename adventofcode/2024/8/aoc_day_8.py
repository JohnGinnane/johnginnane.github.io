import math

print("test") # Visual studio code terminal seems to mess up print()

class vec2:
    x = 0
    y = 0
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    def __neg__(self):
        return vec2(-self.x, -self.y)
    
    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y) 

    def copy(self):
        return vec2(self.x, self.y)

    def rot(self, rad):
        if rad == math.pi/4:
            temp = self.x
            self.x = -self.y
            self.y = temp
            return
        elif rad == -math.pi/4:
            temp = self.x
            self.x = self.y
            self.y = -temp
            return

        self.x = self.x * math.cos(rad) - self.y * math.sin(rad)
        self.y = self.x * math.sin(rad) + self.y * math.cos(rad)

class antenna:
    pos:vec2 = vec2()
    freq = ""

    def __init__(self, pos:vec2, freq:str):
        self.pos = pos
        self.freq = freq

    def __str__(self):
        return "'" + self.freq + "' @ " + str(self.pos)
    
    def __eq__(self, other):
        return self.pos == other.pos and self.freq == other.freq

def findAntinodes(A:vec2, B:vec2, limit=100, max:vec2=None, min:vec2=vec2(0, 0)):
    if A is None or B is None:
        return None
    
    results = []

    # A    =  1, 1
    # B    = -1, 0
    # diff = (1 - -1), (1 - 0)
    #      =  2, 1
    # To go from B to A we need
    # to add diff
    
    # Diff to go from B to A
    diff = A - B

    if max == None:
        # If we add this diff to B again
        # we get B to A antinode
        results.append(A + diff)
        
        # If we subtract this from B
        # we get from A to B antinode
        results.append(B - diff)
    else:        
        # Dimensions were specified
        # so keep adding the diff until
        # we go outside the limits
        working = A + diff
        limit_start = limit

        while (working.x >= min.x and working.x <= max.x and
               working.y >= min.y and working.y <= max.y and
               limit > 0):
            results.append(working)
            limit -= 1
            working += diff

        # Do same but other direction
        working = B - diff
        limit = limit_start

        while (working.x >= min.x and working.x <= max.x and
               working.y >= min.y and working.y <= max.y and
               limit > 0):
            results.append(working)
            limit -= 1
            working -= diff

    return results

antennae = {}
dimensions = vec2(-1, -1)

with open("test_input_08.txt", "r") as freq:
    for y, line in enumerate(freq.readlines()):
        if line.isspace(): continue
        dimensions.y += 1
        tmp_width = -1

        for x, char in enumerate(line):
            if char.isspace(): continue
            tmp_width += 1

            if char == ".": continue

            if char not in antennae:
                antennae[char] = []
            
            antennae[char].append(antenna(vec2(x, y), char))

        if tmp_width > dimensions.x:
            dimensions.x = tmp_width

# Iterate over dictionary and look for antinodes
antinodes = {}

for freq in antennae:
    for i, ant in enumerate(antennae[freq]):
        for j in range(i+1, len(antennae[freq])):
            other_ant = antennae[freq][j]

            print("Antinodes for " + str(ant) + " and " + str(other_ant))
            # Simulate antinodes
            results = findAntinodes(ant.pos, other_ant.pos, 1, dimensions)

            if results is None:
                continue
            
            if freq not in antinodes:
                antinodes[freq] = []

            antinodes[freq] += results

# Count distinct antinode locations
unique = []
for freq in antinodes:
    #result += str(freq) + ": " 

    for an in antinodes[freq]:
        if an not in unique:
            unique.append(an)
        #result += str(an) + ", "
    #result += "\n"

# Part 1: 293
print("Unique antinode locations: " + str(len(unique)))

# Do it all again for part 2, but increase limit of antinodes
antinodes = {}

for freq in antennae:
    for i, ant in enumerate(antennae[freq]):
        for j in range(i+1, len(antennae[freq])):
            other_ant = antennae[freq][j]

            print("Antinodes for " + str(ant) + " and " + str(other_ant))
            # Simulate antinodes
            results = findAntinodes(ant.pos, other_ant.pos, 100, dimensions)

            if results is None:
                continue
            
            if freq not in antinodes:
                antinodes[freq] = []

            antinodes[freq] += results

# Count distinct antinode locations
unique = []
for freq in antinodes:
    print("Harmonic antinodes for '" + str(freq) + "'")
    for an in antinodes[freq]:
        print("\t" + str(an))
        if an not in unique:
            unique.append(an)

# Part 1: 293
print("Unique harmonic antinode locations: " + str(len(unique)))
