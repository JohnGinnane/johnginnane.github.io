# 1. Import rules
# 2. Import updates
# 3. Rules are stored in list:
#    rule_after[79] = [33, 22, 64, 73, 93]
#    rule_before[58] = [79, x, y, z]
# # In this case 58 must proceed 79

rule_after = {}
rule_before = {}
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
            print(str(before) + ": " + str(rule_before[before]))

            if not after in rule_after:
                rule_after[after] = list()
            
            rule_after[after].append(before)

            continue
        
        updates = list(map(int, line.split(",")))

for before in rule_before:
    print("[" + str(before) + "] = " + str(rule_before[before]))
