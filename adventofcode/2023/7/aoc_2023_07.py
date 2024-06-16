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
        "2":  0,
        "3":  1,
        "4":  2,
        "5":  3,
        "6":  4,
        "7":  5,
        "8":  6,
        "9":  7,
        "T":  8,
        "J":  9,
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
        
        # Parse the cards
        for c in cards_str:
            self.cards.append(c)
            if not c in self.summary:
                self.summary[c] = 1
            else:
                self.summary[c] += 1

        # Sort summary
        self.summary = dict(sorted(self.summary.items(), key=lambda item: item[1], reverse=True))

        i = iter(self.summary.values())
        summary_first = next(i)
        summary_second = 0

        if len(self.summary) > 1:
            summary_second = next(i)
        
        self.type = ""

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
        elif len(self.summary) == 5:
            self.type = "H"

    def __str__(self):
        return "Cards: " + "".join([k*v for (k, v) in self.summary.items()]) + ", Bid: " + pad(self.bid, 5) + ", Type; " + self.type + ", Summary: " + ", ".join([str(v)+"x"+k for (k, v) in self.summary.items()])

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

for k in range(len(hands)):
    v = hands[k]
    print(pad(k, 3) + ": " + str(v))
    total_winnings += v.bid * (k+1)

print("Part 1 Total Winnings: " + str(total_winnings))