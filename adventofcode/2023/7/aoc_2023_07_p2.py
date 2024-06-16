import re
import math

def right(s, l):
    return str(s)[-l:]

def left(s, l):
    return str(s)[:l]

def pad(s, l):
    return right(" " * l + str(s), l)

def padr(s, l):
    return left(str(s) + " " * l, l)

class hand:
    card_hierarchy = {
        "J":  0, # WILD CARD
        "2":  1,
        "3":  2,
        "4":  3,
        "5":  4,
        "6":  5,
        "7":  6,
        "8":  7,
        "9":  8,
        "T":  9,
        "Q": 10,
        "K": 11,
        "A": 12
    }

    type_hierarchy = {
        "H": 0, # High Card       (VWXYZ)
        "1": 1, # One Pair        (XX???)
        "2": 2, # Two Pair        (XXYY?)
        "3": 3, # Three of a Kind (XXX??)
        "F": 4, # Full House      (XXXYY)
        "4": 5, # Four of a Kind  (XXXX?)
        "5": 6  # Five of a Kind  (XXXXX)
    }

    def __init__(self, hand_str:str):
        self.hand_str = hand_str.strip()

        cards_str, bid_str = re.search("([A-Z0-9]{5}) ([0-9]+)", self.hand_str).group(1, 2)
        self.cards_str = cards_str
        self.bid = int(bid_str)

        self.cards = []
        self.summary = {}
        self.simulated_summary = {}

        # Parse the cards
        for c in cards_str:
            self.cards.append(c)
            if not c in self.summary:
                self.summary[c] = 1
            else:
                self.summary[c] += 1

        # Sort summary
        #self.summary = dict(sorted(self.summary.items(), key=lambda item: item[1], reverse=True))
        self.simulated_summary = self.summary.copy()

        sumiter = iter(self.simulated_summary.keys())
        most_card = ""
        high_card = ""
        wildcards = 0

        new_summary = {}
        # Handle wildcards
        while True:
            try:
                card = next(sumiter)
                if card == "J":
                    wildcards = self.simulated_summary[card]
                    continue

                new_summary[card] = self.simulated_summary[card]

                if high_card == "":
                    high_card = card
                elif hand.card_hierarchy[card] > hand.card_hierarchy[high_card]:
                    high_card = card

                if most_card == "":
                    most_card = card
                elif self.simulated_summary[card] > self.simulated_summary[most_card]:
                    most_card = card

            except StopIteration:
                break

        self.most_card = most_card
        self.high_card = high_card
        
        if len(new_summary) > 0:
            self.simulated_summary = new_summary.copy()

        if wildcards > 0 and wildcards < 5:
            self.simulated_summary[high_card] += wildcards
            
        self.simulated_summary = dict(sorted(self.simulated_summary.items(), key=lambda item: item[1], reverse=True))
        i = iter(self.simulated_summary.values())
        summary_first = next(i)
        summary_second = 0

        if len(self.simulated_summary) > 1:
            summary_second = next(i)
        
        self.type = "H"

        # Find the type
        if summary_first == 5:
            self.type = "5"
        elif summary_first == 4:
            self.type = "4"
        elif summary_first == 3 and summary_second == 2:
            self.type = "F"
        elif summary_first == 3:
            self.type = "3"
        elif summary_first == 2 and summary_second == 2:
            self.type = "2"
        elif summary_first == 2:
            self.type = "1"

    def __str__(self):
        #output  = "Cards: " + "".join([k*v for (k, v) in self.summary.items()])
        output  = "Cards: " + self.cards_str #"".join([c for c in self.cards])
        output += ", Bid: " + pad(self.bid, 5)
        output += ", Type: " + self.type
        output += ", Summary: " + ", ".join([str(v)+"x"+k for (k, v) in self.simulated_summary.items()])

        return output

    def __eq__(self, other):
        match = True

        for k in range(len(self.cards)):
            if self.cards[k] != other.cards[k]:
                match = False
                break

        return match

    def __lt__(self, other):
        if self == other:
            return False

        if self.type == other.type:
            # Iterate over cards
            # and figure out precedence
            for k in range(len(self.cards)):
                this_card = self.cards[k]
                that_card = other.cards[k]

                if this_card == that_card:
                    # Cards are the same :(
                    continue
                else:
                    return hand.card_hierarchy[this_card] < hand.card_hierarchy[that_card]
        else:
            # Just check type
            return hand.type_hierarchy[self.type] < hand.type_hierarchy[other.type]
        
        return False
    
    def __le__(self, other):
        if self == other:
            return True
        
        return self < other
    
    def __gt__(self, other):
        if self == other:
            return False
        
        return other < self
    
    def __ge__(self, other):
        if self == other:
            return True
        
        return self > other

lines = open("input_07.txt", "r").readlines()
hands = []

for line in lines:
    hands.append(hand(line))

hands.sort()

total_winnings = 0
type_summary = {}

for k in range(len(hands)):
    v = hands[k]

    if not v.type in type_summary:
        type_summary[v.type] = 1
    else:
        type_summary[v.type] += 1
    
    print(pad(k, 3) + ": " + str(v) + " (H: " + v.high_card + ", M: " + v.most_card + ")")
    total_winnings += v.bid * (k+1)

# for t in type_summary:
#     v = type_summary[t]
#     print(t + ": " + str(v))

# JJTA2
# JJ369

# 253,022,409 too low
# 253,413,013 still too low
# 253,995,656 incorrect
# 253,846,975 incorrect
print("Part 2 Total Winnings: " + str(total_winnings))