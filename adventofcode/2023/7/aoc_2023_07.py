import re
import math

def right(s, l):
    return str(s)[-l:]

def left(s, l):
    return str(s)[:l]

def pad(s, l):
    return right(" " * l + str(s), l)

def padr(s, l):
    return left(str(s) + " " * l, l)

class hand:
    def __init__(self, original):
        self.original_string = original

    def __str__(self):
        return self.original_string

lines = open("test_07.txt", "r").readlines()
hands = []

for line in lines:
    hands.append(hand(line.strip()))

for h in hands:
    print(h)