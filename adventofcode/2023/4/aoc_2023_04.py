import re
import math

def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

class card:
    def __init__(self, number, target_numbers, picked_numbers):
        self.number = number
        self.target_numbers = target_numbers
        self.picked_numbers = picked_numbers
        self.winning_numbers = []
        self.points = -1

    def __str__(self):
        output = "Card " + ("   " + str(self.number))[-3:] + ": "

        for num in self.target_numbers:
            output += ("   " + str(num))[-3:]

        output += " |"

        for num in self.picked_numbers:
            output += pad(num, 3) #("   " + str(num))[-3:]

        output += " | Points: " + pad(self.points, 3) #("   " + str(self.points))[-3:]

        output += " | Winning:" 

        for num in self.winning_numbers:
            output += pad(num, 3) #("   " + str(num))[-3:]

        return output
    
    def calculatePoints(self):
        if self.points < 0:
            self.findWinningNumbers()
        
        if len(self.winning_numbers) == 0:
            self.points = 0
        else:
            self.points = int(math.pow(2, len(self.winning_numbers) - 1))
    
    def findWinningNumbers(self):
        for target in self.target_numbers:
            if target in self.picked_numbers:
                self.winning_numbers.append(target)

#lines = open("input_04.txt", "r").readlines()
lines = open("test_04.txt", "r").readlines()
cards = []
pattern = r"Card\s*([0-9]+):((?:\s*[0-9]+)+)\s*\|((?:\s*[0-9]+)+)"

# Interpret the lines and convert to cards
for line in lines:
    line = line.strip()
    match = re.match(pattern, line)
    
    if match:
        card_number = int(match.group(1).strip())
        card_targets_str = match.group(2).strip()
        card_pickings_str = match.group(3).strip()

        target_numbers = []
        picking_numbers = []
        
        for num in re.findall(r"[0-9]+", card_targets_str):
            target_numbers.append(int(num))
        for num in re.findall(r"[0-9]+", card_pickings_str):
            picking_numbers.append(int(num))

        cards.append(card(card_number, target_numbers, picking_numbers))

for c in cards:
    c.calculatePoints()
    print(c)