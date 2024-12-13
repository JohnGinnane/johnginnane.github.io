from copy import copy, deepcopy

class thing:
    value = 0

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "v: " + str(self.value)
    
    def copy(self):
        result = thing(self.value)
        return result
    
outside = thing(5)
items = []
items.append(outside)

print("\n---A---")
print(outside)
print(items[-1])

outside.value = 6
items[-1].value = 4

print("\n---B---")
print(outside)
print(items[-1])

outside_copy = deepcopy(outside)
outside_copy.value = 50
items_copy = deepcopy(items)
items_copy[-1].value = 404

print("\n---C---")
print(outside)
print(outside_copy)
print(items[-1])
print(items_copy[-1])