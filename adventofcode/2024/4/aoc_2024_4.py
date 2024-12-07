data_raw = open("test_input_04.txt").readlines()
data = []


for k, v in enumerate(data_raw):
    data.append(list(v.strip()))

for r in data:
    print(r)