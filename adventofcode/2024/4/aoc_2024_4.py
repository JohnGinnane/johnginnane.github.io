import numpy as np
from scipy.ndimage import rotate
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

def pad_with(vector, pad_width, iaxis, kwargs):
    vector[:pad_width[0]]  = ' '
    vector[-pad_width[1]:] = ' '

with open("test_input_04.txt", "r") as f:
    data_raw = [list(line.strip()) for line in f]

data = np.array(data_raw)

# So one idea would be to take this 2D matrix of data and
# iterate over each position. If there is an "X" there then
# check in all 8 directions and look for "M". If we find
# one then make note of direction, continue to look in that
# direction for "A" and finally "S"

# What if we just did a regex on the original data, rotate
# it 45 degrees (somehow), and then did another regex on
# that, until we do all 8 versions?

# regex can check backwards so we only need to do half the 
# rotations (0, 45, 90, 135)

# (4, 4)
# A B C D
# E F G H
# I J K L
# M N O P

# (4, 7)
# A
# E B
# I F C
# M J G D
# N K H
# O L
# P

# (7, 7)
#    A
#   E B
#  I F C
# M J G D
#  N K H
#   O L
#    P

# M I E A
# N J F B
# O K G C
# P L H D

# for r in data:
#     print(r)


#print(data)
#data = np.pad(data, 6, pad_with)
size = len(data)
data = np.pad(data, ((0, size * 3), (0, size * 3)), mode="constant", constant_values=' ')
#print(data)

# x' = cos(45°) * x - sin(45°) * y
# y' = sin(45°) * x + cos(45°) * y

centerX = len(data[0]) / 2
centerY = len(data) / 2

test = ""
newTest = ""
deg = math.pi / 4
exploded = np.full((size * 4, size * 4), ' ', dtype=str)
rotated = np.full((size * 4, size * 4), ' ', dtype=str)
pad_amt = 5

for y, row in enumerate(data):
    for x, char in enumerate(row):
        if char == ' ':
            continue
        exploded[y*2+size][x*2+size] = char

#print(exploded)

for y, row in enumerate(exploded):
    for x, char in enumerate(row):
        relX = x - centerX
        relY = y - centerY

        newX = (math.cos(deg) * relX - math.sin(deg) * relY) + centerX
        newY = (math.sin(deg) * relX + math.cos(deg) * relY) + centerY
        test += "[" + pad(str(x), pad_amt) + ", " + pad(str(y), pad_amt) + "](" + char + ") "
        round_amt = 3
        newTest += "[" + pad(str(round(newX, round_amt)), pad_amt) + ", " + pad(str(round(newY, round_amt)), pad_amt) + "](" + char + ") "

        if char != ' ':
            rotated[round(newY)][round(newX)] = char
        
    test += "\n"
    newTest += "\n"

# print(test)
# print(newTest)

# print(rotated)

result = ""
for y, row in enumerate(rotated):
    for x, char in enumerate(row):
        result += char
    result += "\n"
print(result)


# #print(test)