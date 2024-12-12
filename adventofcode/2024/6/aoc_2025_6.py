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

def GridToString(grid):
    result = ""
    for row in grid:
        for col in row:
            result += col
        result += "\n"
    return result.strip()

grid = []
width = 0
height = 0
y = 0
x = 0

with open("test_input_06.txt", "r") as f:
    lines = f.readlines()

    for line in lines:
        if len(grid) <= y:
            grid.append([])

        for char in line:
            grid[y].append(char)

            if x > width:
                width = x
            x += 1

        x = 0
        y += 1
        if y > height:
            height = y

guard_pos = vec2(0, 0)
guard_vel = vec2(0, 0)
next_vel = vec2(0, 0)
obstacles = []

print("Width:  " + str(width))
print("Height: " + str(height))

# Find guard and obstacles
for y, row in enumerate(grid):
    for x, char in enumerate(row):

        if char == '^' or char.lower() == 'v' or char == '<' or char == '>':
            guard_pos.x = x
            guard_pos.y = y

            guard_vel.x = 0
            guard_vel.y = 0

            if   char == '^':
                guard_vel.y = -1
            elif char == '>':
                guard_vel.x =  1
            elif char.lower() == 'v':
                guard_vel.y =  1
            elif char == '<':
                guard_vel.x = -1

            next_vel = guard_vel.copy()
            next_vel.rot(math.pi/4)
        elif char == '#':
            obstacles.append(vec2(x, y))

visited = []
previous_obstacles = []

# This is a reverse queue
# The first element is the
# oldest obstacle visited
potential_obstacles = []

while (guard_pos.x >= 0 and guard_pos.x < width and
       guard_pos.y >= 0 and guard_pos.y < height):
    
    print("Guard: " + str(guard_pos))
    # More guard in the direction they are facing until they hit an object
    if not guard_pos in visited:
        visited.append(guard_pos.copy())

    # Check object in front is an obstacle
    try:
        next = grid[guard_pos.y + guard_vel.y][guard_pos.x + guard_vel.x]
    except:
        # Out of bounds means the guard will leave the area
        print("Guard has left the area, last seen at:")
        print("Pos: " + str(guard_pos))
        print("Heading in direction:")
        print("Vel: " + str(guard_vel))
        break

    if (guard_pos + guard_vel) in obstacles:
        previous_obstacles.append(guard_pos + guard_pos)

        # Rotate vel 90 degrees to the right
        guard_vel = next_vel.copy()
        next_vel.rot(math.pi/4)
    else:
        guard_pos += guard_vel

        # Check if a previous obstacle is to our right
        # Run backwards 3x from right side obstacle and 
        # check if we land in the same spot?
        for po in previous_obstacles:
            if ((guard_pos.x - po.x) * next_vel.y -
                (guard_pos.y - po.y) * next_vel.x) == 0:
                potential_obstacles.append(guard_pos + guard_vel)
                print("Pot Obs: " + str(potential_obstacles[-1]))
                break

# Part 1: 5404
print("Distinct locations: "  + str(len(visited)))
print("Potential obstacles: " + str(len(potential_obstacles)))

# For part 2 what I think I should do is
# iterate over the grid as usual, emulating
# the guard's movements. However keep a 
# list of the last 3 obstacle's positions
# Each time we move to check if turning to
# the right here would lead me to the 3rd 
# last obstacle, i.e. creating a loop
# Make a note of the potential new obstacle
# location and then continue as usual