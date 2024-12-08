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

rules = {}
updates = []
mid_page_total = 0
bad_updates = []

def checkReport(update):
    bad_page = -1
    
    i = 0
    while i < len(update) - 1 and bad_page < 0:
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
            if this_page in rules:
                if that_page in rules[this_page]:
                    if i >= j:
                        return i, j

            # Is that page supposed to be before this page?
            if that_page in rules:
                if this_page in rules[that_page]:
                    if j >= i:
                        return i, j
            
            j += 1        
        i += 1

with open("test_input_05.txt", "r") as f:
    lines = f.readlines()

    for line in lines:
        if len(line.strip()) <= 0:
            continue

        if "|" in line:
            rules_raw = list(map(int, line.split("|")))

            # Add the rule to both dicts
            before = rules_raw[0]
            after = rules_raw[1]
            
            if not before in rules:
                rules[before] = list()
            
            rules[before].append(after)

            continue
        
        updates.append(list(map(int, line.split(","))))

for k in range(0, len(updates)):
    update = updates[k]

    #print("Checking " + str(update) + " is in order:")
    bad_pages = checkReport(update)

    if not bad_pages:
        mid_page_total += update[int(len(update)/2)]
    else:
        print("Bad pages " + str(bad_pages))
        bad_updates.append((k))

# Part 1: 5248
print("Mid page total: " + str(mid_page_total) + "\n")

for k in range(0, len(bad_updates)):
    watch = 0

    while True:
        update = updates[bad_updates[k]]

        bad_pages = checkReport(update)

        if bad_pages:
            idx_this = bad_pages[0]
            idx_that = bad_pages[1]

            tmp = update[idx_this]
            update[idx_this] = update[idx_that]
            update[idx_that] = tmp
        else:
            break

        watch += 1
        if watch >= 100:
            print("Watchdog met!")
            break

    print("Fixed report: " + str(updates[bad_updates[k]]))