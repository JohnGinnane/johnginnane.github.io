data = []

with open("test_input_07.txt", "r") as f:
    for line in f.readlines():
        parts = line.split(":")
        total = int(parts[0])
        components = []
        for c in parts[1].split(" "):
            if len(c.strip()) <= 0:
                continue
            components.append(int(c.strip()))
        
        if len(components) > 0:
            data.append((total, components))

print(data[0][1])

for line in data:
    p = ""
    for component in line[1]:
        if p != "":
            p += " ? "
        p += str(component)
    p = str(line[0]) + " = " + p
    print(p)

# Method 1: Et tu, Brute Force?
# Iterate over each line
# Compile a list of all possible combinations
# of each component multiplied and/or added
# to each other component. Sort of a factorial?
# e.g. C [1, 2, 3]:
#    1 + 2 + 3 =  6
#    1 + 2 x 3 =  7
#    1 x 2 + 3 =  5
#    1 x 2 x 3 =  6

# Method 2: Binary Search Tree??
# Basically start with all numbers added
# together. If we need to go higher than multiply
# If too high then try next component instead
# If too low then move to next component