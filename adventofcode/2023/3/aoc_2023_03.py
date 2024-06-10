import re
import math

class part:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = int(value)
        self.width = len(value)
        self.isPart = False

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "] " + str(self.value) + " (" + str(self.width) + ")" + " Part: " + str(self.isPart)

class symbol:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.ratio = 0
        self.touched = 0

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "] " + self.symbol + ", ratio: " + str(self.ratio)

lines = open("input_03.txt", "r").readlines()
#lines = open("test_03.txt", "r").readlines()
parts = []
symbols = []

parts_index = {}
symbols_index = {}

y = 0

for line in lines:
    # read over the line from left to right
    buffer = ""
    buffer_x = 0
    
    x = 0
    for c in line:
        if re.match("[0-9]", c):
            if buffer == "":
                buffer_x = x
                
            buffer += c
        else:
            if buffer != "":
                parts.append(part(buffer_x, y, buffer))
            
            buffer = ""

            if c != "." and not c.isspace():
                symbols.append(symbol(x, y, c))
        
        x += 1

    buffer = ""
    y += 1

# Loop through all parts and put them into a list of lists
# The index of the outer list corresponds to the line the
# part belongs to in the original data
for k in range(len(parts)):
    v = parts[k]
    line = v.y
    if not line in parts_index:
        parts_index[line] = []

    parts_index[line].append(k)

for k in range(len(symbols)):
    v = symbols[k]
    line = v.y

    if not line in symbols_index:
        symbols_index[line] = []

    symbols_index[line].append(k)

# Now iterate over the indices and check for adjacency
# between parts and symbols

# For each line of parts
#     For each part in line (via index)
#         For each line (previous, current, next)
#             For each symbol in line (via index)
#                 If symbol.x is close to part.x then mark part

for part_line in parts_index:    
    parts_on_line = parts_index[part_line]
    
    for part_index in parts_on_line:
        part = parts[part_index]
        # If part was already marked then go next
        if part.isPart:
            continue
    
        # Now look at neighbouring
        # lines (above, on, below)
        # for symbols
        line_min = max(part_line - 1, 0)
        line_max = part_line + 1
        
        for symbol_line in range(line_min, line_max + 1):
            # No symbols on this line
            if not symbol_line in symbols_index:
                continue
            
            symbols_on_line = symbols_index[symbol_line]
            
            for symbol_index in symbols_on_line:
                symbol = symbols[symbol_index]

                # check if symbol is within X distance
                if symbol.x >= part.x - 1 and symbol.x <= part.x + part.width:
                    part.isPart = True
                    break
            
            if part.isPart:
                break

total_sum = 0

# Part 1 - Sum total parts
for part in parts:
    if part.isPart:
        total_sum += part.value

print("Sum of Parts: " + str(total_sum))

# Part 2 - Do the inverse of the above loop
# Iterate over symbols, then iterate over
# neighbouring parts
for symbol_line in symbols_index:
    symbols_on_line = symbols_index[symbol_line]

    for symbol_index in symbols_on_line:
        symbol = symbols[symbol_index]

        # We're only interested in 'gears'
        if symbol.symbol != "*":
            continue

        # Now look for neighbouring numbers
        line_min = max(symbol_line - 1, 0)
        line_max = symbol_line + 1

        for part_line in range(line_min, line_max + 1):
            # No parts on this line
            if not part_line in parts_index:
                continue

            parts_on_line = parts_index[part_line]

            for part_index in parts_on_line:
                part = parts[part_index]
                
                # Check if part is within distance
                if symbol.x >= part.x - 1 and symbol.x <= part.x + part.width:
                    symbol.touched += 1
                    
                    if symbol.ratio == 0:
                        symbol.ratio = part.value
                    else:
                        symbol.ratio *= part.value

total_ratio = 0
for symbol in symbols:
    if symbol.symbol == "*" and symbol.touched > 1:
        #print(symbol)
        total_ratio += symbol.ratio

print("Total Ratio: " + str(total_ratio))
