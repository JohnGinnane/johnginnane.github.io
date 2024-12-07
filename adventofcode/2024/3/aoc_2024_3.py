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
regex_mul = re.compile(r"(mul\(([0-9]{1,3}(,|))+\))")
param_mul = re.compile(r"([0-9]{1,3})")

muls = re.findall(regex_mul, input)

# Count number of parameters instances
dict_param = {}

grand_total = 0
for m in muls:
    params = re.findall(param_mul, m[0])

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
print("Grand Total: " + str(grand_total))