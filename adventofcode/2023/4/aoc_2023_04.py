import re
import math

class card:
    def __init__(self, number, winning_numbers, picked_numbers):
        self.number = number
        self.winning_numbers = winning_numbers
        self.picked_numbers = picked_numbers

    def __str__(self):
        output = "Card " + str(self.number) + ": "

        for num in self.winning_numbers:
            output += ("   " + str(num))[-3:]

        output += " | "

        for num in self.picked_numbers:
            output += ("   " + str(num))[-3:]

        return output

#lines = open("input_04.txt", "r").readlines()
lines = open("test_04.txt", "r").readlines()
cards = []
pattern = r"Card\s*([0-9]+):((?:\s*[0-9]+)+)\s*\|((?:\s*[0-9]+)+)"

for line in lines:
    line = line.strip()
    match = re.match(pattern, line)
    
    if match:
        card_number = int(match.group(1).strip())
        card_winning_str = match.group(2).strip()
        card_pickings_str = match.group(3).strip()

        winning_numbers = []
        picking_numbers = []
        
        for num in re.findall(r"[0-9]+", card_winning_str):
            winning_numbers.append(int(num))
        for num in re.findall(r"[0-9]+", card_pickings_str):
            picking_numbers.append(int(num))

        cards.append(card(card_number, winning_numbers, picking_numbers))

for c in cards:
    print(c)