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

with open("test_input_04b.txt", "r") as f:
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

def rotate(arr, deg):
    size = len(data)
    arr_pad = np.pad(arr, ((0, size * 3), (0, size * 3)), mode="constant", constant_values=' ')

    # x' = cos(45°) * x - sin(45°) * y
    # y' = sin(45°) * x + cos(45°) * y

    centerX = len(arr_pad[0]) / 2
    centerY = len(arr_pad) / 2

    arr_expl = np.full((size * 4, size * 4), ' ', dtype=str)
    arr_rota = np.full((size * 4, size * 4), ' ', dtype=str)

    for y, row in enumerate(arr_pad):
        for x, char in enumerate(row):
            if char == ' ':
                continue
            arr_expl[y*2+size][x*2+size] = char

    for y, row in enumerate(arr_expl):
        for x, char in enumerate(row):
            relX = x - centerX
            relY = y - centerY

            newX = (math.cos(deg) * relX - math.sin(deg) * relY) + centerX
            newY = (math.sin(deg) * relX + math.cos(deg) * relY) + centerY

            if char != ' ':
                arr_rota[round(newY)][round(newX)] = char
        
    return arr_rota

rotated = rotate(data, math.pi / 2)

result = ""
for y, row in enumerate(rotated):
    for x, char in enumerate(row):
        result += char
    result += "\n"
print(result)


# #print(test)