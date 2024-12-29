num = 1234
num_str = str(num)
left = num_str[0:int(len(num_str)/2)]
right = num_str[int(len(num_str)/2):]

print("Left:  " + left)
print("Right: " + right)