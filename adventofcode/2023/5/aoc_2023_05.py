import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class map:
    def __init__(self, from_type, from_id, to_type, to_id, range):
        self.from_type = from_type
        self.from_id = from_id
        self.to_type = to_type
        self.to_id = to_id
        self.range = range