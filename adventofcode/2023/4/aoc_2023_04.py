import re
import math

#lines = open("input_04.txt", "r").readlines()
lines = open("test_04.txt", "r").readlines()

pattern = r"Card\s*([0-9]+):((?:\s*[0-9]+)+)\s*\|((?:\s*[0-9]+)+)"

for line in lines:
    line = line.strip()
    match = re.match(pattern, line)
    
    if match:
        card_number = int(match.group(1).strip())
        card_winning = match.group(2).strip()
        card_pickings = match.group(3).strip()

        print(card_number)
        print(card_winning)
        print(card_pickings)