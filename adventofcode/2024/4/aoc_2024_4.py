import numpy as np
from scipy.ndimage import rotate

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

print(data)
data = np.pad(data, 2, pad_with)
print(data)

centerX = len(data[0]) / 2
centerY = len(data) / 2
print("Center: [" + str(centerX) + ", " + str(centerY) + "]")

# #print(test)