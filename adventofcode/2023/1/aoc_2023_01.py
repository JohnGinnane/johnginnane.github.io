import re

nummap = {
    "1": 1,
    "one": 1,
    "2": 2,
    "two": 2,
    "3": 3,
    "three": 3,
    "4": 4,
    "four": 4,
    "5": 5,
    "five": 5,
    "6": 6,
    "six": 6,
    "7": 7,
    "seven": 7,
    "8": 8,
    "eight": 8,
    "9": 9,
    "nine": 9
}

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

def getFirstAndLastNumber(string):
    first = 0;
    last = 0;
    pattern = r"((one|two|three|four|five|six|seven|eight|nine)|[0-9])"

    # I tried to use regex to find both the first and last
    # numbers, but in case of "oneight" it would match "one"
    # and not "eight" :(

    s = re.findall(pattern, string)
    
    if (len(s) > 0):
        first = int(nummap[s[0][0]])
        last = first

    # Search for from, expand from end of string, e.g.
    # hello worlD
    # hello worLD
    # hello woRLD
    found = False
    length = len(string)
    
    for i in range(0, length):
        s = re.findall(pattern, string[length-i-1:])
        if (len(s) > 0):
            last = int(nummap[s[0][0]])
            break        

    #print(debug)
    return first * 10 + last

#Lines = ("1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet")
#Lines = ("two1nine",
#         "eightwothree",
#         "abcone2threexyz",
#         "xtwone3four",
#         "4nineeightseven2",
#         "zoneight234",
#         "7pqrstsixteen")
Lines = open("input.txt", "r").readlines()
#Lines = ("1sevenseven7ld", "hello", "threetxgc2htprtqqj5fouroneightlf")

part_1_total = 0
part_2_total = 0
index = 0

for line in Lines:
    line = line.strip()
    index += 1
    digit = getFirstAndLastDigit(line)
    number = getFirstAndLastNumber(line)
    print(str(index) + " - " + line + ": " + str(digit) + ", " + str(number))
    part_1_total += digit
    part_2_total += number

print("---------")
print(part_1_total)
print(part_2_total)
