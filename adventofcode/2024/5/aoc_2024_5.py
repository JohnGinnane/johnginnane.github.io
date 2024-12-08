print("test")

# 1. Import rules
# 2. Import updates
# 3. Rules are stored in list:
#    rule_after[79] = [33, 22, 64, 73, 93]
#    rule_before[58] = [79, x, y, z]
# # In this case 58 must precede 79
# 4. Iterate over each update
# 5. Check if num satisifies its rules
#    by comparing it against subsequent numbers
#    If no rule present check the opposite page
#    and make sure it shouldn't precede this num

rule_after = {}
rule_before = {}
updates = []
mid_page_total = 0

with open("input_05.txt", "r") as f:
    lines = f.readlines()

    for line in lines:
        if len(line.strip()) <= 0:
            continue

        if "|" in line:
            rules_raw = list(map(int, line.split("|")))

            # Add the rule to both dicts
            before = rules_raw[0]
            after = rules_raw[1]
            
            if not before in rule_before:
                rule_before[before] = list()
            
            rule_before[before].append(after)
            #print(str(before) + ": " + str(rule_before[before]))

            if not after in rule_after:
                rule_after[after] = list()
            
            rule_after[after].append(before)

            continue
        
        updates.append(list(map(int, line.split(","))))

# for before in rule_before:
#     print("[" + str(before) + "] = " + str(rule_before[before]))

for k in range(0, len(updates)):
    update = updates[k]

    #print("Checking " + str(update) + " is in order:")
    update_good = True

    i = 0
    while i < len(update) - 1 and update_good:
        this_page = update[i]

        # if this_page in rule_before:
        #     print("Rules for " + str(this_page) + ": " + str(rule_before[this_page]))
        # else:
        #     print("No before rules for " + str(this_page))

        j = 0
        while j < len(update):
            # Ignore checking this page against itself
            if j == i:
                j += 1
                continue
            
            #print("\t" + str(j+1) + "/" + str(len(update)))
            that_page = update[j]

            # Should this page be before that page?
            if this_page in rule_before:
                if that_page in rule_before[this_page]:
                    if i >= j:
                        update_good = False
                        #print("Page " + str(this_page) + " should precede " + str(that_page))
                        break

            # Is that page supposed to be before this page?
            if that_page in rule_before:
                if this_page in rule_before[that_page]:
                    if j >= i:
                        update_good = False
                        break
            
            #print("\tNo rules for " + str(this_page) + " and " + str(that_page))
            
            j += 1        
        i += 1

    if update_good:
        print("Update " + str(update) + " is in order")
        mid_page_total += update[int(len(update)/2)]
    else:
        print("Update " + str(update) + " is NOT in order")

# Part 1: 5248
print("Mid page total: " + str(mid_page_total))