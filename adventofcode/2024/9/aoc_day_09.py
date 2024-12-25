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
            tmp = self.data[a_idx]
            self.data[a_idx] = self.data[b_idx]
            self.data[b_idx] = tmp

    def __str__(self):
        result = ""

        for d in self.data:
            if d is None:
                result += "."
            else:
                result += str(d)

        return result

    def compress(self):
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
        i = len(self.data) - 1
        while i > end:
            #print("i: " + str(i) + ", end: " + str(end))

            # Look for free space starting at the left
            # most side of condensed data and ending at 
            # index we're trying to move out from
            for j in range(end, i):
                if i == j:
                    continue

                if self.data[i] is None:
                    continue

                if self.data[j] is None and self.data[i] is not None:
                    #print("Moving " + str(i) + " into " + str(j))
                    end = j
                    self.data[j] = self.data[i]
                    self.data[i] = None
                    break

            i -= 1

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
            if last_id != id:
                ptr = pointer(start_idx, last_id, i - start_idx)

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
my_disk.compress()
print(my_disk)

#my_disk.compress()
# # This takes a long time to run
# # Not sure how to speed it up (yet)
# disk = condenseList(disk)
#my_disk = condenseListContiguous(disk)

# Part 1: 6258319840548 (amazing, first go!)
# 11696163753804 is too high!
# 11654871070704 is still too high
print("Checksum: " + str(my_disk.checksum()))