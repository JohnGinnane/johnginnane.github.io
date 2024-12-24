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
        #print(pad(i, 6) + "/" + str(len(map)))

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
    i = len(result) - 1
    while i > end:
        #print("i: " + str(i) + ", end: " + str(end))

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

        i -= 1

    return result

def listToString(L:list):
    if L is None: 
        return ""
    
    result = "(" + str(len(L)) + ") "

    for k, v in enumerate(L):
        if v is None:
            result += "-"
        else:
            result += str(v)

    return result

def condenseListContiguous(L:list):
    result = L.copy()

    # Start with the highest file ID (rightmost file)
    # and attempt to fit it into the leftmost space
    # Move down the IDs until we hit the lowest
    id = None
    last_id = None
    size = 0
    lowest_move_id = None

    for i in range(len(result)-1, -1, -1):
        last_id = id
        id = result[i]

        if id == last_id or i == len(result) - 1:
            size += 1

        if last_id != id and last_id is not None and i < len(result) - 1:
            # if lowest_move_id is not None:
            #     if last_id > lowest_move_id:
            #         continue
            
            print("Looking to move " + str(last_id))
            #print("Looking for " + str(size) + " spaces for " + str(last_id))
            # We just finished iterating over a file
            # Look for spaces starting from the left
            space = findSpace(result, size)
            #print("Found " + str(space))

            # Couldn't find enough space for this file
            # go next
            if space is None:
                size = 1
                continue

            # If space is on or after this index then 
            # go next
            if space >= i:
                size = 1
                continue

            #print("Before:   " + listToString(result))
            del result[space:space+size]
            result[space:space] = [last_id] * size
            del result[i+1:i+1+size]
            result[i+1:i+1] = [None] * size
            #print("\t" + listToString(result))

            # Make note of this ID so we don't try to move it in the future
            lowest_move_id = last_id
            
            size = 1

    return result

def findSpace(L:list, size:int = 1):
    start_index = None
    id = None
    space_size = 0

    for i in range(0, len(L)):
        id = L[i]

        if id is None:
            space_size += 1
            
            if start_index is None:
                start_index = i
        elif id is not None:
            space_size = 0
            start_index = None

        if space_size >= size:
            return start_index
        
    return None

def checksum(L:list):
    checksum = 0

    for k, v in enumerate(L):
        if v is None:
            continue
        
        #print(str(k) + "*" + str(v) + "=" + str(k*v))
        checksum += k*v

    return checksum

# print(mapToString("12345"))
# print(mapToString())

example_str = "2333133121414131402"
example = mapToList(example_str)

# # print(", ".join(map(str, mapToList("12345"))))
# print("Start:\t" + listToString(example))
# # print(", ".join(map(str, condenseList(mapToList("12345")))))
# #print(", ".join(map(str, condenseList(example))))
example = condenseListContiguous(example)
# print("End:\t" + listToString(example))
print("Checksum: " + str(checksum(example)))
# disk_str = ""

with open("input_09.txt", "r") as f:
    disk_str = f.readline().strip()

# example = mapToList("2333133121414131402")
# example = condenseList(example)
# print("Example checksum: " + str(checksum(example)))

# disk = mapToList(disk_str)
# # This takes a long time to run
# # Not sure how to speed it up (yet)
# # disk = condenseList(disk)
# disk = condenseListContiguous(disk)

# Part 1: 6258319840548 (amazing, first go!)
# 11696163753804 is too high!
# 11654871070704 is still too high
#print("Checksum: " + str(checksum(disk)))