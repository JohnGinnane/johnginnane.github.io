print("Day 11:\n")

import math
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool

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
              right("00" + str(td.seconds) , 2) + ".")
    
    if td.microseconds >= 0 and milliseconds == 0:
        result = "<" + result + "001"
    else:
        result = " " + result + right("000" + str(milliseconds), 3)

    return result

def applyRules(L:list, debug:bool=False, start_index:int=0, end_index=None):
    if start_index >= len(L): return []
    if start_index < 0: start_index = 0
    if end_index is None: end_index = len(L)-1
    if end_index < start_index: end_index = len(L)-1
    if end_index > len(L)-1: end_index = len(L)-1

    result = L.copy()    
    if len(result) <= 0: return []

    i = 0
    length=int(math.log10(len(result)))+1

    while i <= end_index:
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
            end_index += 1
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
with open("input_11.txt", "r") as f:
    stones = list(map(int, f.read().split(" ")))

print("Start: " + " ".join(list(map(str, stones))))
start_time = datetime.now()
ts = datetime.now()

# test: 55312

# Part 1: 189167 stones
for i in range(0, 28):
    from_index = 0
    to_index = int(len(stones)/2)-1
    ##print("From: " + str(from_index) + " to: " + str(to_index))

    #stones = applyRules(stones)
    
    # left_half = applyRules(stones[from_index:to_index])
    # right_half = applyRules(stones[to_index:])
    # stones = left_half + right_half

    pool = ThreadPool(processes=2)
    left_async = pool.apply_async(applyRules, (stones[from_index:to_index],))
    right_async = pool.apply_async(applyRules, (stones[to_index:],))
    left_half = left_async.get()
    right_half = right_async.get()
    stones = left_half + right_half
    
    newts = datetime.now()
    
    #print(pad(i+1, 3) + ") (" + formatTimeDelta(newts-ts) + ") " + str(len(stones)) + " stones")

    ts = newts

# Part 1: 189167
print("Total stones: " + str(len(stones)))
print("Total time: " + formatTimeDelta(datetime.now()-start_time))