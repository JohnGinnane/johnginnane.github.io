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

    def __init__(self, hand_str:str):
        self.hand_str = hand_str.strip()

        cards_str, bid_str = re.search("([A-Z0-9]{5}) ([0-9]+)", self.hand_str).group(1, 2)
        self.cards_str = cards_str
        self.bid = int(bid_str)

        self.cards = []
        self.summary = {}
        
        for c in cards_str:
            self.cards.append(c)
            if not c in self.summary:
                self.summary[c] = 1
            else:
                self.summary[c] += 1

        self.cards.sort(key=lambda x: hand.card_hierarchy[x], reverse=True)
        self.summary = dict(sorted(self.summary.items(), key=lambda item: item[1], reverse=True))        

    def __str__(self):
        return "Cards: " + "".join(self.cards) + ", Bid: " + pad(self.bid, 5) + ", Summary: " + ", ".join([str(v)+"x"+k for (k, v) in self.summary.items()])

lines = open("test_07.txt", "r").readlines()
hands = []

for line in lines:
    hands.append(hand(line))

for h in hands:
    print(h)