def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

data = []

with open("input_07.txt", "r") as f:
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

for line in data:
    p = ""
    for component in line[1]:
        if p != "":
            p += " ? "
        p += str(component)
    p = str(line[0]) + " = " + p

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
# Treat each operator as a bit within a
# base number, i.e. base 2 for + and *
# The + is 0 and * is 1
# Starting at 0, count up to how ever many
# bits can be fit into operator spaces and 
# check the sum
# e.g. 1 _ 2 _ 3
# Operator # Binary = Decimal
#    ++    =   00   =   0
#    +*    =   01   =   1
#    *+    =   10   =   2
#    **    =   11   =   3

# Method 2: Binary Search Tree??
# Basically start with all numbers added
# together. If we need to go higher than multiply
# If too high then try next component instead
# If too low then move to next component

# Method 3: Work Backwards
# Try to divide total by each component
# If remainder then move onto next component
# If no remainder then check if the 
# difference is sum of remaining components
# If not then check next component for remainder
print("test")

# Least significant bit to most
GLO_OPERATORS = ["+", "*"]

# Taken from https://stackoverflow.com/a/28666223
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def Dec2Op(dec, pad=0):
    # Convert decimal number into list
    # of operators from most to least
    # significant
    # e.g. 013 -> 0000 1101 -> ++++ **+*
    bits = numberToBase(dec, len(GLO_OPERATORS))
    result = [GLO_OPERATORS[0]] * len(bits)

    for k, v in enumerate(bits):
        result[k] = GLO_OPERATORS[v]

    while len(result) < pad:
        result.insert(0, GLO_OPERATORS[0])

    return result

def method1(total, numbers, debug=False):
    if debug: print(str(total) + " ?= " + str(numbers))
    #perms = len(numberToBase(len(numbers), 2))
    # GLO_OPERATORS = ["+", "*"] => len() = 2
    # numbers = [900, 4, 8] => len() = 3
    # 2^3 = 8
    # 0: ["+", "+", "+"]
    # 1: ["+", "+", "*"]
    # 2: ["+", "*", "+"]
    # 3: ["+", "*", "*"]
    # 4: ["*", "+", "+"]
    # 5: ["*", "+", "*"]
    # 6: ["*", "*", "+"]
    # 7: ["*", "*", "*"]
    
    len_ops = len(GLO_OPERATORS)
    perms = pow(len_ops, 1 + len(numberToBase(len(numbers), len_ops)))
    if debug: print("Permutations: " + str(perms))
    operators = []

    for i in range(0, perms):
        operators.append(Dec2Op(i, len(numbers)-1))
    if debug: 
        for o in operators:
            print(o)

    for o in operators:
        sum = numbers[0]
        string = str(numbers[0])

        for i in range(1, len(numbers)):
            match o[i-1]:
                case "+":
                    sum += numbers[i]
                    string += " + " + str(numbers[i])
                case "*":
                    sum *= numbers[i]
                    string += " * " + str(numbers[i])

        # End once we find the total
        if sum == total:
            return (sum, string)

    return None

# results = method1(data[0][0], data[0][1], True)
# for r in results:
#     print(r)

total_correct = 0
incorrects = []

for k,v in enumerate(data):
    result = method1(v[0], v[1])
    
    printout = pad(k+1, len(str(len(data)))) + "/" + str(len(data)) + " "
    if result != None:
        printout += str(result[0]) + " = "  + result[1]
        total_correct += result[0]
    else:
        printout += "Unable to find sum for " + str(v[0]) + " with " + str(v[1])
        incorrects.append((k, v))
    
    #print(printout)

# 2840782 -- too low??
# 2607489241 -- still too low
# 1537595512443 -- STILL TOO LOW????
print("Total Correct: " + str(total_correct))

# Sort by smallest total asc
incorrects.sort(key=lambda n: n[1][0])
# Sort by number of elements asc
#incorrects.sort(key=lambda n: len(n[1][1]))

for i in range(0, 20):
    print(incorrects[i])

# n = 334
# result = method1(data[n][0], data[n][1], True)
# print(result)

# print(data[115][1])
# print(len(data[115][1]))
# print(numberToBase(len(data[115][1]), 2))
# print(pow(len(GLO_OPERATORS),len(numberToBase(len(data[115][1]), 2))))