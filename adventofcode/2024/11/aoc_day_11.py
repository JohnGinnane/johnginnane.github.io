print("Day 11:\n")

import math
from datetime import datetime, timedelta

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

def split(S:str):
    left = S[0:int(len(S)/2)]
    right = S[int(len(S)/2):]
    return left, right

split_dict = {}

def formatTimeDelta(td:timedelta):
    result = ""

    minutes = int(td.seconds/60)
    hours = int(minutes/60)
    milliseconds = int(td.microseconds/1000)

    result = (str(hours) + ":" + 
              right("00" + str(minutes), 2) + ":" +
              right("00" + str(td.seconds) , 2) + ":")
    
    if td.microseconds > 0 and milliseconds == 0:
        result = "<" + result + "001"
    else:
        result = " " + result + right("000" + str(milliseconds), 3)

    return result

def applyRules(L:list, debug:bool=False):
    result = L.copy()

    i = 0
    length =int(math.log10(len(result)))+1

    while i < len(result):
        ts = datetime.now()

        if debug: print(pad(i+1, length) + "/" + str(len(result)) + ":")
        # Rules:
        #  1. If number is 0 then change to 1
        if result[i] == 0:
            if debug: print("\tRule 1) Replacing 0 with 1")
            result[i] = 1
            i += 1
            if debug: print("\tTook " + formatTimeDelta(datetime.now()-ts))
            continue

        #  2. If number is even then, split into 2 numbers
        #     where the left half digits go left, right go right
        #     No leading zeroes, e.g. "1000" -> "10" and "0"
        if int(math.log10(result[i])+1) % 2 == 0:
            num_str = str(result[i])
            if debug: print("\tRule 2) Splitting " + num_str)
            
            # look for split dict
            if result[i] in split_dict:
                result.insert(i+1, split_dict[result[i]][1])
                result[i] = split_dict[result[i]][0]
            else:
                left = int(num_str[0:int(len(num_str)/2)])
                right = int(num_str[int(len(num_str)/2):])
                split_dict[result[i]] = (left, right)
                result[i] = left
                result.insert(i+1, right)
            i += 2
            if debug: print("\tTook " + formatTimeDelta(datetime.now()-ts))
            continue

        #  3. If no rules applied at this stage then multiply
        #     by 2024
        if debug: print("\tRule 3) Muliplying by 2024")
        result[i] *= 2024
        i += 1
        if debug: print("\tTook " + formatTimeDelta(datetime.now()-ts))

    return result

stones = []
with open("test_input_11.txt", "r") as f:
    stones = list(map(int, f.read().split(" ")))

print("Start: " + " ".join(list(map(str, stones))))
#start_time = datetime.timestamp(datetime.now())
ts = datetime.now()


# Part 1: 189167 stones
for i in range(0, 30):
    stones = applyRules(stones)
    newts = datetime.now()
    
    print(pad(i+1, 3) + ") (" + formatTimeDelta(newts-ts) + ") " + str(len(stones)) + " stones")

    ts = newts