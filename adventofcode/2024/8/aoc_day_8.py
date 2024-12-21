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

class antenna:
    pos:vec2 = vec2()
    freq = ""

    def __init__(self, pos:vec2, freq:str):
        self.pos = pos
        self.freq = freq

    def __str__(self):
        return "'" + self.freq + "' @ " + str(self.pos)

antennae = []

with open("test_input_08.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, char in enumerate(line):
            if char.isspace(): continue
            if char == ".": continue

            antennae.append(antenna(vec2(x, y), char))

for a in antennae:
    print(a)