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
        "2":  2,
        "3":  3,
        "4":  4,
        "5":  5,
        "6":  6,
        "7":  7,
        "8":  8,
        "9":  9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
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
        
        # Parse he cards
        for c in cards_str:
            self.cards.append(c)
            if not c in self.summary:
                self.summary[c] = 1
            else:
                self.summary[c] += 1

        # Sort cards and summary
        self.cards.sort(key=lambda x: hand.card_hierarchy[x], reverse=True)
        self.summary = dict(sorted(self.summary.items(), key=lambda item: item[1], reverse=True))

        i = iter(self.summary.values())
        summary_first = next(i)
        summary_second = 0

        if len(self.summary) > 1:
            summary_second = next(i)
        
        self.type = ""
        print(str(summary_first) + ", " + str(summary_second))

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
        return "Cards: " + "".join(self.cards) + ", Bid: " + pad(self.bid, 5) + ", Type; " + self.type + ", Summary: " + ", ".join([str(v)+"x"+k for (k, v) in self.summary.items()])

lines = open("test_07.txt", "r").readlines()
hands = []

for line in lines:
    hands.append(hand(line))

for h in hands:
    print(h)