lines = open("input_01.txt", "r").readlines()
current_number = 50
zeroOnEnd = 0
zeroTotal = 0
last_number = current_number

print("The dial starts by pointing at 50.")
debugPrint = ""

for line in lines:
    direction = line[:1]
    distance = int(line[1:])

    zeroTotal += int(distance/100.0)
    distance = distance % 100

    if (direction == "R"):
        current_number = current_number + distance
    else:
        current_number = current_number - distance

    while current_number < 0:
        current_number += 100

        if last_number != 0:
            zeroTotal += 1
            last_number = 0

    while current_number >= 100:
        current_number -= 100

        if last_number != 0:
            zeroTotal += 1
            last_number = 0

    if current_number == 0:
        zeroOnEnd += 1
    
    # Need to track last number so if we 
    # move off 0 we dont count it twice     
    last_number = current_number

    debugPrint += f"The dial is rotated {(line.strip()+"    ")[:5]} to point at {(str(current_number)+" ")[:2]}."

    debugPrint += f" {zeroOnEnd}/{zeroTotal} -> {zeroOnEnd + zeroTotal}"

    print(debugPrint)
    debugPrint = ""

    # The dial starts by pointing at 50.
    # The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
    # The dial is rotated L30 to point at 52.
    # The dial is rotated R48 to point at 0.
    # The dial is rotated L5 to point at 95.
    # The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
    # The dial is rotated L55 to point at 0.
    # The dial is rotated L1 to point at 99.
    # The dial is rotated L99 to point at 0.
    # The dial is rotated R14 to point at 14.
    # The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.

