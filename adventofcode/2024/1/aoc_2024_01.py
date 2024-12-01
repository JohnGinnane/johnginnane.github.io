def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

lines = open("input_01.txt", "r").readlines()
left_list = []
right_list = []

for line in lines:
    ids = list(filter(None, line.split(" ")))
    left_list.append(int(ids[0]))
    right_list.append(int(ids[1]))

# Simply sort lists from smallest to largest
left_list.sort()
right_list.sort()

total_dist = 0

for i in range(0, len(left_list)):
    print(right("   " + str(i+1), 4) + "/" + str(len(left_list)) + " - L: " + str(left_list[i]) + ", R: " + str(right_list[i]))
    total_dist += abs(left_list[i] - right_list[i])

# 1765812
print("Total Distance: " + str(total_dist))

# Part 2
# Iterate over left list
# Find number of instances of that number in
# right list and add to "similarity_score"
similarity_score = 0

for k in range(0, len(left_list)):
    v = left_list[k]

    # Use python's "count" function to find number of occurrences of "v" in "right_list"
    occurs = right_list.count(v)
    print(right("    " + str(k+1), 4) + "/" + str(len(left_list)) + " - Number " + str(v) + " appears " + str(occurs) + " times in right list")
    similarity_score += (v * occurs);

# 20520794
print("Similarity Score: " + str(similarity_score))