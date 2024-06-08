import re

def getFirstAndLastDigit(string):
    first = 0;
    last = 0;
    m = re.search("[^0-9]*([0-9]).*", string)
    if (m):
        first = int(m.group(1))
        last = first

    m = re.search("[^0-9]*([0-9]).*", string[::-1])
    if (m):
        last = int(m.group(1))

    return first * 10 + last

#Lines = ("1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet")
Lines = open("input.txt", "r").readlines()  

total = 0
for line in Lines:
    n = getFirstAndLastDigit(line)
    print(n)
    total += n

print(total)
