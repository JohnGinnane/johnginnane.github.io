import math
from copy import copy, deepcopy

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class vec2:
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

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

class grid:
    grid = []
    width = 0
    height = 0
    obstacles = []

    def __init__(self, *str):
        self.grid = []
        self.width = 0
        self.height = 0
        y = 0
        x = 0

        if str is None:
            return
    
        if len(str) <= 0:
            return

        lines = str[0].split("\n")

        for line in list(lines):
            if len(line.strip()) <= 0:
                continue
            
            if len(self.grid) <= y:
                self.grid.append([])

            for char in line:
                self.grid[y].append(char)

                if char == '#':
                    self.obstacles.append(vec2(x, y))

                x += 1
                if x > self.width:
                    self.width = x

            x = 0
            y += 1

            if y > self.height:
                self.height = y

    def __str__(self):
        result = ""
        for row in self.grid:
            for col in row:
                result += col
            result += "\n"
        return result.strip()

    def find(self, char:chr):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.grid[y][x] == char:
                    return vec2(x, y)

    def at(self, vec):
        if (vec.x < 0 or vec.x >= self.width or
            vec.y < 0 or vec.y >= self.height):
            return None
        
        return self.grid[vec.y][vec.x]
    
    def inBounds(self, pos):
        return (pos.x >= 0 and 
                pos.x < self.width and
                pos.y >= 0 and
                pos.y < self.height)

    # def copy(self):
    #     result = grid()
    #     result.grid = deepcopy(self.grid)
    #     result.width = self.width
    #     result.height = self.height
    #     result.obstacles = self.obstacles.copy()
    #     return result

    def addObstacle(self, pos):
        if not self.inBounds(pos):
            return
        
        self.grid[pos.y][pos.x] = '#'
        self.obstacles.append(pos)

def getVel(char:chr):
    if char == '^':
        return vec2( 0, -1)
    elif char == '>':
        return vec2( 1,  0)
    elif char == 'v' or char == 'V':
        return vec2( 0,  1)
    elif char == '<':
        return vec2(-1,  0)
    
    return None

the_grid = None

with open("input_06.txt", "r") as f:
    the_grid = grid(f.read())

#guard_pos = the_grid.find()
guard_pos = None

for c in ['^', '>', 'v', 'V', '<']:
    res = the_grid.find(c)
    if res is not None:
        guard_pos = res
        guard_vel = getVel(the_grid.grid[res.y][res.x])
        break

print("Guard pos: " + str(guard_pos))
print("Guard vel: " + str(guard_vel))
print("Width:  " + str(the_grid.width))
print("Height: " + str(the_grid.height))

visited = []
potential_obstacles = []

while the_grid.inBounds(guard_pos):

    # More guard in the direction they are facing until they hit an object
    if not guard_pos in visited:
        visited.append(guard_pos.copy())

    if the_grid.at(guard_pos+guard_vel) == '#':
        # Rotate vel 90 degrees to the right
        guard_vel.rot(math.pi/4)
    else:
        if len(visited) > 1:
            # Simulate if there was an obstacle right in front of us
            grid_clone = deepcopy(the_grid)
            guard_pos_clone = guard_pos.copy()
            guard_vel_clone = guard_vel.copy()
            grid_clone.addObstacle(guard_pos_clone + guard_vel_clone)

            hit_obstacles = []
            loop = False

            while grid_clone.inBounds(guard_pos_clone):
                if grid_clone.at(guard_pos_clone+guard_vel_clone) == '#':
                    pos_and_vel = (guard_pos_clone + guard_vel_clone, guard_vel_clone)

                    # Check if we already hit this obstacle
                    if pos_and_vel in hit_obstacles:
                        loop = True
                        break
                    else:
                        hit_obstacles.append(pos_and_vel)

                    guard_vel_clone.rot(math.pi/4)
                else:
                    guard_pos_clone += guard_vel_clone

            if loop:
                potential_obstacles.append(guard_pos+guard_vel)
                print("v: " + pad(len(visited), 5) + ". Found potential obstacle: " + str(potential_obstacles[-1]))

        guard_pos += guard_vel

# Part 1: 5404
print("Distinct locations: "  + str(len(visited)))

# Part 2: 2920 -- Too high!
print("Potential obstacles: " + str(len(potential_obstacles)))
