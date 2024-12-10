class thing:
    value = 0

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return "v: " + str(self.value)
    
outside = thing(5)
items = []
items.append(outside)

print("A:\n")
print(outside)
print(items[-1])

outside.value = 6
items[-1].value = 4

print("B:\n")
print(outside)
print(items[-1])