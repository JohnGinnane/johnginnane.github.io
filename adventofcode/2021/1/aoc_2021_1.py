def base10toN(value, base, usenumerics=True, excel=False):
    if excel:
        usenumerics = False

    if (not excel and value < base) or (excel and value <= base):
        if usenumerics:
            if value == 0:
                return "0"
            elif value <= 9:
                return str(value)
            else:
                return chr(64+value-9)
        else:
            if value == 0:
                return "Z"
            else:
                return chr(64+value)
    
    div, rem = divmod(value, base)
    thisdigit = ""
    
    if rem == 0:
        if usenumerics:
            return base10toN(div, base, usenumerics) + "0"
        else:
            return base10toN(div, base, usenumerics) + "Z"
    else:
        thisdigit = ""
        if usenumerics:
            if rem <= 9:
                thisdigit = str(rem)
            else:
                thisdigit = chr(64+rem-9)
        else:
            thisdigit = chr(64+rem)

        return base10toN(div, base, usenumerics) + thisdigit

file1 = open('input_01.txt', 'r')
Lines = file1.readlines()

# Part 1 Vars
# depth = 0
# lastdepth = 0
# output = ""
# inc = 0
# dec = 0

# Part 2 Vars
sumdepth = 0
lastsumdepth = 0
output2 = ""
suminc = 0
sumdec = 0
sumnochange = 0

i = 1
window = []

for line in Lines:
    depth = int(line)
    sumdepth = 0
    output = str(i) + "/" + str(len(Lines)) + " "  + line.strip() + " "

    # Part 2 Logic
    output2 = str(i) + "/" + str(len(Lines)) + " " + base10toN(i, 26, True) + ": "

    window.append(depth)
    
    if len(window) > 2:
        while len(window) > 3:
            window.pop(0)
        
        sumdepth = window[0] + window[1] + window[2]

        output2 = str(i) + "/" + str(len(Lines)) + " " + base10toN(i-2, 26, False)
        output2 += ": {0} ({1}, {2}, {3}) ".format(sumdepth, window[0], window[1], window[2])

        if lastsumdepth == 0:
            output2 += "(N/A - no previous measurement)"
        else:
            if sumdepth - lastsumdepth > 0:
                output2 += "(increased)"
                suminc += 1
            elif sumdepth - lastsumdepth < 0:
                output2 += "(decreased)"
                sumdec += 1
            else:
                output2 += "(no change)"
                sumnochange += 1
        
        lastsumdepth = sumdepth

        if i/len(Lines) <= 0.02 or i/len(Lines) >= 0.99:
            print(output2)
        
    # Part 1 Logic
    # if lastdepth == 0:
    #     output += "(N/A - no previous measurement)"
    # else:
    #     if depth - lastdepth > 0:
    #         output += "(increased)"
    #         inc += 1
    #     elif depth - lastdepth < 0:
    #         output += "(decreased)"
    #         dec += 1
    #     else:
    #         output += "(no change)"
    # lastdepth = depth

    i+=1
    print(output)

# Part 1 Output
# print("Increases: " + str(inc))
# print("Decreases: " + str(dec))
# print("    Total: " + str(inc - dec))

# Part 2 Output
print("Sum Increases: " + str(suminc))
print("Sum Decreases: " + str(sumdec))
print("Sum No Change: " + str(sumnochange))
print("    Sum Total: " + str(suminc - sumdec))