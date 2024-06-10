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

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "] " + self.symbol

lines = open("input_03.txt", "r").readlines()
#lines = open("test2_03.txt", "r").readlines()
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

for part_line in parts_index:    
    parts_on_line = parts_index[part_line]
    #print("line: " + str(part_line))
    
    for part_index in parts_on_line:
        part = parts[part_index]
        # If part was already marked then go next
        if part.isPart:
            continue
        
        #print("\tpart: " + str(part))

        # Now look at neighbouring lines for this part
        line_min = max(part_line - 1, 0)
        line_max = part_line + 1
        
        #print(str(line_min) + " - " + str(line_max))
        
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
last_line = 0
debug = ""
line_total = 0

for part in parts:
    if part.isPart:
        total_sum += part.value

##for k in range(len(parts)):
##    v = parts[k]
##    
##    if last_line != v.y:
##        if debug != "":
##            print(debug + " = " + str(line_total))
##        line_total = 0
##        debug = ""
##
##    last_line = v.y
##    
##    if v.isPart:
##        if debug != "":
##            debug += " + "
##        debug += str(v.value)
##            
##        line_total += v.value
##        total_sum += v.value

print("Sum of Parts: " + str(total_sum))
