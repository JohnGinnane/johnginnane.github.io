print("test")

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

with open("input_06.txt", "r") as f:
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

guard_pos = dict(x=0, y=0)
guard_vel = dict(x=0, y=0)

print("Width:  " + str(width))
print("Height: " + str(height))

# find guard
for y, row in enumerate(grid):
    for x, char in enumerate(row):

        if char == '^' or char.lower() == 'v' or char == '<' or char == '>':
            guard_pos["x"] = x
            guard_pos["y"] = y

            guard_vel["x"] = 0
            guard_vel["y"] = 0

            if   char == '^':
                guard_vel["y"] = -1
            elif char == '>':
                guard_vel["x"] =  1
            elif char.lower() == 'v':
                guard_vel["y"] =  1
            elif char == '<':
                guard_vel["x"] = -1
            
            break

visited = []

while (guard_pos["x"] >= 0 and guard_pos["x"] < width and
       guard_pos["y"] >= 0 and guard_pos["y"] < height):
    # More guard in the direction they are facing until they hit an object
    if not (guard_pos["x"], guard_pos["y"]) in visited:
        visited.append((guard_pos["x"], guard_pos["y"]))

    # Check object in front is an obstacle
    try:
        next = grid[guard_pos["y"] + guard_vel["y"]][guard_pos["x"] + guard_vel["x"]]
    except:
        # Out of bounds means the guard will leave the area
        print("Guard has left the area, last seen at:")
        print("Pos: [" + str(guard_pos["x"]) + ", " + str(guard_pos["y"]) + "]")
        print("Heading in direction:")
        print("Vel: [" + str(guard_vel["x"]) + ", " + str(guard_vel["y"]) + "]")
        break

    if next == '#':
        # Rotate vel 90 degrees to the right
        temp = guard_vel["x"]
        guard_vel["x"] = -guard_vel["y"]
        guard_vel["y"] =  temp
    else:
        guard_pos["x"] += guard_vel["x"]
        guard_pos["y"] += guard_vel["y"]

# Part 1: 5404
print("Distinct locations: " + str(len(visited)))

# For part 2 what I think I should do is
# iterate over the grid as usual, emulating
# the guard's movements. However keep a 
# list of the last 3 obstacle's positions
# Each time we move to check if turning to
# the right here would lead me to the 3rd 
# last obstacle, i.e. creating a loop
# Make a note of the potential new obstacle
# location and then continue as usual