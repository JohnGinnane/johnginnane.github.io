print("Day 10:\n")

import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

# Iterates over a list and returns a tuple of
# key, value, and key formatted like "xx/yy"
def foreach(L:list):
    length = int(math.log10(len(L)))+1

    for i in range(0, len(L)):
        idx = pad(i+1, length) + "/" + str(len(L))
        key = i
        value = L[i]

        yield key, value, idx

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

    def __hash__(self):
        return hash((hash(self.x), hash(self.y)))

class trail:
    origin:vec2
    dest:vec2
    score:int

    def __init__(self, origin:vec2 = None, dest:vec2 = None):
        self.origin = origin
        self.dest = dest
        self.score = 0

    def __eq__(self, other):
        return self.origin == other.origin and self.dest == other.dest
    
    def __str__(self):
        result  = "Origin: "  + str(self.origin)
        result += ", Dest: "  + str(self.dest)
        result += ", Score: " + str(self.score)

        return "[" + result + "]"

class topmap:
    raw_data:str = ""
    grid:list = []
    trailheads:list = []
    neighbours = [
        vec2(-1,  0),
        vec2( 0,  1),
        vec2( 1,  0),
        vec2( 0, -1)
    ]

    def __init__(self, map_str:str):
        y = -1
        self.raw_data = map_str

        for line in map_str.split():
            y += 1

            for char in line:
                while y >= len(self.grid):
                    self.grid.append([])

                if char.isdigit():
                    self.grid[y].append(int(char))
                else:
                    self.grid[y].append(-1)

        self.findTrailheads()

        # Once we find all trailheads then
        # iterate over them and find all
        # destinations for them
        while True:
            # Find first trail with no destination
            th:trail = None

            for t in self.trailheads:
                if t.dest is None:
                    th=t
                    break

            if th is None:
                break

            self.__navigatePath(th, th.origin)

        self.__scorePath()


    def __str__(self):
        result = ""
        for y in range(0, len(self.grid)):
            if result != "": result += "\n"
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] < 0:
                    result += "."
                else:
                    result += str(self.grid[y][x])
        return result
    
    def at(self, pos:vec2):
        if pos is None: 
            return

        x = pos.x
        y = pos.y

        if x < 0 or y < 0: return
        if y >= len(self.grid): return
        if x >= len(self.grid[y]): return
            
        return self.grid[y][x]

    def findTrailheads(self):
        self.trailheads = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] == 0:
                    self.trailheads.append(trail(vec2(x, y)))
        
    def findValueAround(self, value, pos:vec2):
        result = []
        
        for n in self.neighbours:
            try:
                check = pos + n

                if self.at(check) == value:
                    result.append(check)
            except:
                continue

        return result
    
    def findPaths(self):
        result = 0

        for th in self.trailheads:
            result += self.__findPathsAt(th, th.origin, [])

        return result

    def __navigatePath(self, th:trail, pos:vec2):
        if th is None: return
        this_value = self.at(pos)

        # When we hit the peak
        if this_value == 9:
            # If this trail doesn't already have 
            # a destination then set it
            if th.dest is None:
                th.dest = pos
            else:
                # If it does have a destination
                # then create a new trail
                pot_new = trail(th.origin, pos)
                if pot_new not in self.trailheads:
                    self.trailheads.append(pot_new)
        else:
            # Find neighbours with next value
            for r in self.findValueAround(this_value+1, pos):
                self.__navigatePath(th, r)

    def __scorePath(self, th:trail=None, pos:vec2=None):
        if th is None:
            for th in self.trailheads:
                self.__scorePath(th, th.origin)
            return
        
        this_value = self.at(pos)
        if this_value == 9:
            th.score += 1
        else:
            for r in self.findValueAround(this_value+1, pos):
                self.__scorePath(th, r)

    def __findPathsAt(self, th:trail, pos:vec2, history:list):
        if th is None: return

        result = 0

        this_value = self.at(pos)
        history.append(pos)

        if this_value == 9:
            th.score += 1
            
            if th.dest is None:
                th.dest = pos
                return 1
            
            return 0
        elif this_value < 9:
            for r in self.findValueAround(this_value+1, pos):
                #if r in history: continue

                result += self.__findPathsAt(th, r, history)

        return result

map = None
with open("input_10.txt", "r") as f:
    map = topmap(f.read())
    
print(map)

origins = {}
for th in map.trailheads:
    if th.origin not in origins:
        origins[th.origin] = (0, th.score)

    origins[th.origin] = (origins[th.origin][0]+1, th.score) # How many dests for this origin?

print("Trailheads: " + str(len(origins)))

total_score = 0
total_rating = 0
for k, v in enumerate(origins):
    print(str(k+1) + ") Origin: " + str(v) + " - Score: " + str(origins[v][0]) + ", Rating: " + str(origins[v][1]))
    total_score += origins[v][0]
    total_rating += origins[v][1]

# Part 1: 472
print("Total Score: " + str(total_score)) # Number of destinations for each origin
# Part 2: 969
print("Total Rating: " + str(total_rating)) # Number of different routes from origin to same destination