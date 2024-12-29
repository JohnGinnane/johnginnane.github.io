print("Day 11:\n")

stones = []
with open("test_input_11.txt", "r") as f:
    stones = list(map(int, f.read().split(" ")))

for k, v in enumerate(stones):
    print(str(k+1) + ") " + str(v))