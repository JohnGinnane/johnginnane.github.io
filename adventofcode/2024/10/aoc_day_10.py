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

    def __findPathsAt(self, trail:trail, pos:vec2, history:list):
        if trail is None: return

        result = 0

        this_value = self.at(pos)
        history.append(pos)

        if this_value == 9:
            trail.score += 1
            
            if trail.dest is None:
                trail.dest = pos
                return 1
            
            return 0
        elif this_value < 9:
            for r in self.findValueAround(this_value+1, pos):
                #if r in history: continue

                result += self.__findPathsAt(trail, r, history)

        return result

map = None
with open("input_10.txt", "r") as f:
    map = topmap(f.read())
    
print(map)

# Part 1: 472
print("Found paths: " + str(map.findPaths()))

# for k, v, kstr in foreach(map.trailheads):
#     print(kstr + " - " + str(v))

print("Trailheads: " + str(len(map.trailheads)))
sum_rating = 0
for th in map.trailheads:
    sum_rating += th.score
print("Sum rating: " + str(sum_rating))