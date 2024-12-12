import math

print("test")

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

        if str is not None:
            lines = str[0].split("\n")

            for line in list(lines):
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

with open("test_input_06.txt", "r") as f:
    the_grid = grid(f.read())

#guard_pos = the_grid.find()
guard_pos = None

for c in ['^', '>', 'v', 'V', '<']:
    res = the_grid.find(c)
    if res is not None:
        guard_pos = res
        break

guard_vel = getVel(the_grid.grid[guard_pos.y][guard_pos.x])

print("Guard pos: " + str(guard_pos))
print("Guard vel: " + str(guard_vel))
print("Width:  " + str(the_grid.width))
print("Height: " + str(the_grid.height))

visited = []

while (guard_pos.x >= 0 and guard_pos.x < the_grid.width and
       guard_pos.y >= 0 and guard_pos.y < the_grid.height):

    # More guard in the direction they are facing until they hit an object
    if not guard_pos in visited:
        visited.append(guard_pos.copy())

    if the_grid.at(guard_pos+guard_vel) == '#':
        # Rotate vel 90 degrees to the right
        guard_vel.rot(math.pi/4)
    else:
        guard_pos += guard_vel

        # # Check if a previous obstacle is to our right
        # # Run backwards 3x from right side obstacle and 
        # # check if we land in the same spot?
        # for po in previous_obstacles:
        #     if ((guard_pos.x - po.x) * next_vel.y -
        #         (guard_pos.y - po.y) * next_vel.x) == 0:
        #         potential_obstacles.append(guard_pos + guard_vel)
        #         print("Pot Obs: " + str(potential_obstacles[-1]))
        #         break

# Part 1: 5404
print("Distinct locations: "  + str(len(visited)))
#print("Potential obstacles: " + str(len(potential_obstacles)))

# For part 2 what I think I should do is
# iterate over the grid as usual, emulating
# the guard's movements. However keep a 
# list of the last 3 obstacle's positions
# Each time we move to check if turning to
# the right here would lead me to the 3rd 
# last obstacle, i.e. creating a loop
# Make a note of the potential new obstacle
# location and then continue as usual