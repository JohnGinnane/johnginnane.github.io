import re

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

def sign(n:int):
    if n < 0:
        return -1    
    if n > 0:
        return 1    
    return 0

input = open("input_03.txt", "r").read()

# Count instances of mul(
input_mul = re.compile(r"(do\(\)|don't\(\)|mul\(([0-9]{1,3}(,|))+\))")
regex_mul = re.compile(r"(mul\(([0-9]{1,3}(,|))+\))")
param_mul = re.compile(r"([0-9]{1,3})")

instruct = re.findall(input_mul, input)

# Count number of parameters instances
dict_param = {}
enabled = True

grand_total = 0
for i in instruct:
    params = re.findall(param_mul, i[0])

    # Check if it's a do or don't
    if i[0] == "do()":
        enabled = True
    elif i[0] == "don't()":
        print(i[0])
        enabled = False

    if not enabled:
        continue

    print(i[0])    

    if len(params) < 2:
        continue

    if not (len(params) in dict_param.keys()):
        dict_param[len(params)] = 1
    else:
        dict_param[len(params)] += 1
    
    #   print(str(m) + " -> " + str(params))
    total = 1
    for n in params:
        total *= int(n)
    grand_total += total
    
    #print(m[0] + " = " + str(total))

print(dict_param)

# 171183259 -- too high
# Part 1: 171183089
# Part 2: 63866497 -- first try qB^]
print("Grand Total: " + str(grand_total))