print("Day 11:\n")

import math

def split(S:str):
    left = S[0:int(len(S)/2)]
    right = S[int(len(S)/2):]
    return left, right

def applyRules(L:list, debug:bool=False):
    result = L.copy()

    i = 0
    while i < len(result):
        # Rules:
        #  1. If number is 0 then change to 1
        if result[i] == 0:
            if debug: print("Rule 1) Replacing 0 with 1")
            result[i] = 1
            i += 1
            continue

        #  2. If number is even then, split into 2 numbers
        #     where the left half digits go left, right go right
        #     No leading zeroes, e.g. "1000" -> "10" and "0"
        if int(math.log10(result[i])+1) % 2 == 0:
            num_str = str(result[i])
            if debug: print("Rule 2) Splitting " + num_str)
            left = num_str[0:int(len(num_str)/2)]
            right = num_str[int(len(num_str)/2):]
            result[i] = int(left)
            result.insert(i+1, int(right))
            i += 2
            continue

        #  3. If no rules applied at this stage then multiply
        #     by 2024
        if debug: print("Rule 3) Muliplying by 2024")
        result[i] *= 2024
        i += 1

    return result

stones = []
with open("input_11.txt", "r") as f:
    stones = list(map(int, f.read().split(" ")))

print("Start: " + " ".join(list(map(str, stones))))

# Part 1: 189167 stones
for i in range(0, 25):
    stones = applyRules(stones)
    #print(str(i+1) + ") " + " ".join(list(map(str, stones)))
    print(str(i+1) + ") " + str(len(stones)) + " stones")