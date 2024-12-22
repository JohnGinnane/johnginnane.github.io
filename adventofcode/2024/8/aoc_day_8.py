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

def findAntinodes(A:vec2, B:vec2, max:vec2, min:vec2=vec2(0, 0), part2:bool = False):
    if A is None or B is None or max is None:
        return None
    
    if A == B:
        return None
    
    results = []

    if min is None:
        min = vec2()

    # A    =  1, 1
    # B    = -1, 0
    # diff = (1 - -1), (1 - 0)
    #      =  2, 1
    # To go from B to A we need
    # to add diff
    
    # Diff to go from B to A
    diff = A - B

    if not part2:
        # If we add this diff to B again
        # we get B to A antinode
        results.append(A + diff)
        
        # If we subtract this from B
        # we get from A to B antinode
        results.append(B - diff)

        for i in range(len(results)-1, -1, -1):
            if (results[i].x < min.x or results[i].x > max.x or
                results[i].y < min.y or results[i].y > max.y):
                results.pop(i)
    else:        
        # Dimensions were specified
        # so keep adding the diff until
        # we go outside the limits
        working = A

        while (working.x >= min.x and working.x <= max.x and
               working.y >= min.y and working.y <= max.y):
            results.append(working)
            working += diff

        # Do same but other direction
        working = B

        while (working.x >= min.x and working.x <= max.x and
               working.y >= min.y and working.y <= max.y):
            results.append(working)
            working -= diff

    return results

antennae = {}
dimensions = vec2(-1, -1)

# Read in the grid data
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
            results = findAntinodes(ant.pos, other_ant.pos, dimensions)

            if results is None:
                continue
            
            if freq not in antinodes:
                antinodes[freq] = []

            antinodes[freq] += results

# Sort each frequency's antinode list to help read
for freq in antinodes:
    antinodes[freq].sort(key=lambda an: an.y * dimensions.x + an.x)

# Count distinct antinode locations
unique = []
result = ""
for freq in antinodes:
    result += str(freq) + ": " 

    for an in antinodes[freq]:
        if an not in unique:
            unique.append(an)
        result += str(an) + ", "
    result += "\n"
print(result)

# Part 1: 293
print("Unique antinode locations: " + str(len(unique)))
quit()

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
