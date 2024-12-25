print("Day 9:")

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class pointer:
    index:int = 0
    id:int = None # None means blank space
    size:int = 0

    def __init__(self, index:int, id:int = None, size:int = 1):
        self.index = index
        self.id = id
        self.size = size

    def __str__(self):
        result = "@" + pad(self.index, 5) + ", id: "
        if self.id is None:
            result += "."
        else:
            result += str(self.id)
        result += ", len: " + str(self.size)

        return "[" + result + "]"

class disk:
    data:list
    space_index:list
    file_index:list

    def __init__(self, map:str=None):
        self.data = []

        if map is not None:
            self.data = disk.mapToList(map)

        self.buildIndex()

    def swap(self, a_idx:int, b_idx:int, size:int = 1):
        for i in range(0, size):
            tmp = self.data[a_idx+i]
            self.data[a_idx+i] = self.data[b_idx+i]
            self.data[b_idx+i] = tmp

    def __str__(self):
        result = ""

        for d in self.data:
            if d is None:
                result += "."
            else:
                result += str(d)

        return result

    def compress(self):
        # Compress data by moving files on the right side
        # to free space on the left. The result of this
        # function will mean all the data is on the left
        # as one contiguous space, and then all of the
        # free space is on the rest of the disk

        # Two indices:
        #   1. Right to Left - File Data
        #   2. Left to Right - Free Space
        file_index = len(self.data) - 1
        space_index = 0
        
        while file_index > space_index:
            # If there is no data at this place,
            # decrement file index and go next
            if self.data[file_index] is None:
                file_index -= 1
                continue

            # If there WAS data at that place,
            # check if there is space at the
            # space index, if there is no space
            # then increment space, go next
            if self.data[space_index] is not None:
                space_index += 1
                continue

            # At this point there is space at 
            # space index, and data at file
            # index so just swap
            self.swap(file_index, space_index)

    def compressKeepWhole(self):
        # Compress data by moving files on the right side
        # to free space on the left. The result of this
        # function will mean all the data on the right 
        # that can fit into spaces on the left will be
        # moved over, so more data is left-sided, but still
        # leave many small spaces

        # This time we will refer to our disk indexes to
        # help find spare space. However this means we'll
        # have to rebuild the indexes every time we do a 
        # swap
        
        lowest_id = None
        for file in self.file_index:
            print(file.index)

            for space in self.space_index:
                if space.index >= file.index:
                    continue
                
                if space.size >= file.size:
                    if lowest_id is None:
                        file.id
                    else:
                        if file.id < lowest_id:
                            lowest_id = file.id
                    
                    #print("Swapping " + str(file.size) + " file data at " + str(file.index) + " (" + str(self.data[file.index:file.index+file.size]) + ") with space at " + str(space.index))
                    self.swap(file.index, space.index, file.size)
                    self.buildIndex()
                    break

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

    def buildIndex(self):
        # Iterate over the entire data set
        # and create a list of files and
        # spaces, represented by a pointer
        self.space_index = []
        self.file_index = []

        id = None
        last_id = None
        start_idx = 0

        if len(self.data) <= 1:
            return

        for i in range(1, len(self.data)):
            last_id = self.data[i-1]
            id = self.data[i]

            # If the id changes then we need to 
            # denote that last block as either
            # a file or space block
            last = i == len(self.data)-1

            if last_id != id or last:
                ptr = pointer(start_idx, last_id, i - start_idx + (1 if last else 0))

                if last_id is None:
                    self.space_index.append(ptr)
                else:
                    self.file_index.append(ptr)
                
                # Reset the start index, for
                # this new block
                start_idx = i

        # Sort space index from closest to
        # start of disk to further (L -> R)
        self.space_index.sort(key=lambda p: p.index)

        # Sort file index backwards from
        # furthest from start of disk to
        # closest (R -> L)
        self.file_index.sort(key=lambda p: p.index, reverse=True)

    def checksum(self):
        checksum = 0

        for k, v in enumerate(self.data):
            if v is None:
                continue
            
            #print(str(k) + "*" + str(v) + "=" + str(k*v))
            checksum += k*v

        return checksum

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
            # If we've already checked this ID 
            # then go next
            if lowest_move_id is not None:
                if last_id > lowest_move_id:
                    size = 1
                    continue
            
            lowest_move_id = last_id

            print("Looking for " + pad(size, 3) + " spaces for '" + str(last_id) + "'")
            # We just finished iterating over a file
            # Look for spaces starting from the left
            space = findSpace(result, size)
            #print("Found at " + str(space))

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

disk_str = "2333133121414131402"
#disk_str = "12345"

with open("input_09.txt", "r") as f:
    disk_str = f.readline().strip()

my_disk = disk(disk_str)

print(my_disk)
#my_disk.compress()
my_disk.compressKeepWhole()
print(my_disk)

# Part 1: 6258319840548 (amazing, first go!)
# Part 2: 6286182965311
print("Checksum: " + str(my_disk.checksum()))