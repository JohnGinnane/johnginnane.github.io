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

# Simply sort lists for now
left_list.sort()
right_list.sort()

total_dist = 0

for i in range(0, len(left_list)):
    print(right("   " + str(i+1), 4) + "/" + str(len(left_list)) + " - L: " + str(left_list[i]) + ", R: " + str(right_list[i]))
    total_dist += abs(left_list[i] - right_list[i])

# 1765812
print("Total Distance: " + str(total_dist))