print("Day 10:\n")

class topmap:
    raw_data:str = ""
    grid:list = []
    trailheads:list = []
    neighbours = [
        (-1,  0),
        ( 0,  1),
        ( 1,  0),
        ( 0, -1)
    ]

    def __init__(self, map_str:str):
        x = -1
        y = -1
        self.raw_data = map_str

        for line in map_str.split():
            y += 1
            x = -1

            for char in line:
                x += 1

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
    
    def at(self, pos:tuple):
        return self.at(pos[0], pos[1])

    def at(self, x:int, y:int):
        if x < 0 or y < 0: return
        if y >= len(self.grid): return
        if x >= len(self.grid[y]): return
            
        return self.grid[y][x]

    def findTrailheads(self):
        self.trailheads = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] == 0:
                    self.trailheads.append((x, y))
        
    def findValueAround(self, value, pos:tuple):
        result = []
        
        for n in self.neighbours:
            try:
                x = pos[0] + n[0]
                y = pos[1] + n[1]

                if self.at(x, y) == value:
                    result.append((x, y))
            except:
                continue

        return result
    
map = topmap("0123\n1234\n8765\n9876")
print(map)
map.findTrailheads()

# for th in map.trailheads:
#     print(th)

for r in map.findValueAround(3, (2, 0)):
    print(r)