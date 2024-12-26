print("Day 10:\n")

import math

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
                    self.trailheads.append(vec2(x, y))
        
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
            result += self.__findPathsAt(th, [])

        return result

    def __findPathsAt(self, pos:vec2, history:list):
        result = 0

        this_value = self.at(pos)
        history.append(pos)

        if this_value == 9:
            return 1
        elif this_value < 9:
            for r in self.findValueAround(this_value+1, pos):
                if r in history: continue

                result += self.__findPathsAt(r, history)

        return result

map = None
with open("test_input_10.txt", "r") as f:
    map = topmap(f.read())
    
print(map)
map.findTrailheads()
print("Found paths: " + str(map.findPaths()))

# Iterate over all trailheads
# For each one, look for next numbers
# Iterate over these neighbours and do
# it again and again until we hit 9
