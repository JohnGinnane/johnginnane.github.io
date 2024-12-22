print("Day 9:")

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

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

    for i, char in enumerate(map):
        print(pad(i, 6) + "/" + str(len(map)))

        if reading_file:
            for i in range(0, int(char)):
                result.append(id)
            id += 1
        else:
            for i in range(0, int(char)):
                result.append(None)
        
        reading_file = not reading_file

    return result

def condenseList(L:list):
    result = L.copy()
    # Index at which we stop looking for 
    # free space. As we condense items 
    # to the left we can move the end 
    # forward (i.e. closer) to the right
    end = 0

    # Iterate back from end of list toward the front
    # As we condense data the "end" will move up from
    # 0 to the last element moved to condense the list
    # This element's new position is the right most side
    # of the condensed data, so we don't need to search
    # to the left of this index
    for i in range(len(result)-1, end, -1):
        print("i: " + str(i) + ", end: " + str(end))

        # Look for free space starting at the right
        # most side of condensed data and ending at 
        # index we're trying to move out from
        for j in range(end, i):
            if i == j:
                continue

            if result[i] is None:
                continue

            if result[j] is None and result[i] is not None:
                #print("Moving " + str(i) + " into " + str(j))
                end = j
                result[j] = result[i]
                result[i] = None
                break

    return result   

def checksum(L:list):
    checksum = 0

    for k, v in enumerate(L):
        if v is None:
            continue
        
        #print(str(k) + "*" + str(v) + "=" + str(k*v))
        checksum += k*v

    return checksum

# print(mapToString("12345"))
# print(mapToString("2333133121414131402"))

# print(", ".join(map(str, mapToList("12345"))))
# print(", ".join(map(str, mapToList("2333133121414131402"))))
# print(", ".join(map(str, condenseList(mapToList("12345")))))
# print(", ".join(map(str, condenseList(mapToList("2333133121414131402")))))

disk_str = ""

with open("input_09.txt", "r") as f:
    disk_str = f.readline().strip()

# example = mapToList("2333133121414131402")
# example = condenseList(example)
# print("Example checksum: " + str(checksum(example)))

disk = mapToList(disk_str)
disk = condenseList(disk)

# Part 1: 6258319840548 (amazing, first go!)
print("Checksum: " + str(checksum(disk)))