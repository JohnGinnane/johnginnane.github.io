print("Day 9:")

def mapToString(map:str):
    # Converts the map "12345" to "0..111....22222"
    reading_file = True
    disk = ""
    id = 0

    for char in map:
        if reading_file:
            disk += str(id) * int(char)
            id += 1
        else:
            disk += "." * int(char)

        reading_file = not reading_file

    return disk

def mapToList(map:str):
    reading_file = True
    result = []
    id = 0

    for char in map:
        if reading_file:
            for i in range(0, int(char)):
                result.append(id)
            id += 1
        else:
            for i in range(0, int(char)):
                result.append(None)
        
        reading_file = not reading_file

    return result

print(mapToString("12345"))
print(mapToString("2333133121414131402"))

print(", ".join(map(str, mapToList("12345"))))