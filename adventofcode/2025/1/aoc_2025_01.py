lines = open("input_01.txt", "r").readlines()
current_number = 50
zeroHits = 0

print("The dial starts by pointing at 50.")
debugPrint = ""

for line in lines:
    direction = line[:1]
    distance = int(line[1:])

    if (direction == "R"):
        current_number = current_number + distance
    else:
        current_number = current_number - distance

    while current_number < 0:
        current_number += 100

    current_number = current_number % 100

    debugPrint += f"The dial is rotated {(line.strip()+"    ")[:5]} to point at {current_number}."

    if current_number == 0:
        zeroHits = zeroHits + 1
        debugPrint += f" Hit zero {zeroHits} times!"

    print(debugPrint)
    debugPrint = ""


    # The dial starts by pointing at 50.
    # The dial is rotated L68 to point at 82.
    # The dial is rotated L30 to point at 52.
    # The dial is rotated R48 to point at 0.
    # The dial is rotated L5 to point at 95.
    # The dial is rotated R60 to point at 55.
    # The dial is rotated L55 to point at 0.
    # The dial is rotated L1 to point at 99.
    # The dial is rotated L99 to point at 0.
    # The dial is rotated R14 to point at 14.
    # The dial is rotated L82 to point at 32.
