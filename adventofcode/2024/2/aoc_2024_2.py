def right(s, l):
    return str(s)[-l:]

def pad(s, l):
    return right(" " * l + str(s), l)

def sign(n:int):
    if n < 0:
        return -1    
    if n > 0:
        return 1    
    return 0

def determineSafety(levels, direction):
    if len(levels) == 0:
        return True

    for k in range(1, len(levels)):
        v = levels[k]
        diff = v - levels[k-1]

        # Report is safe if all levels are increasing AND
        # the difference is at least 1 and at most 3
        at_least = 1
        at_most = 3
        if not(abs(diff) >= at_least and abs(diff) <= at_most and sign(diff) == sign(direction)):
            return False
    
    return True

class report:
    effective_details = []
    details = []
    diff = []
    direction = 0
    safe = False

    def __init__(self, data_str:str):
        self.details = list(map(int, data_str.split(" ")))        
        self.safety = 1
        self.safe = True
        self.direction = 0

        if len(self.details) <= 0:
            return
        
        if len(self.details) == 1:
            return 
                
        self.getDiff()
        self.getDir()
        self.getSafety()

        # Iterate up from 0 to n with i
        # Check if details(0:i) is safe
        # If unsafe more than once then unsafe

        # what if we checked both sides of a level to see which 
        # number is best to delete?
        # 9 13 16 17 20
        # for i in range(1, len(self.details) - 2, 1):
        #     prev = self.details[i-1]
        #     cur = self.details[i]
        #     next = self.details[i+1]

        #     if prev == cur

    def __str__(self):
        result = "Report: "
        result += pad("[" + ", ".join(list(map(str, self.details))), 35) + "]"

        result += ", Dir: " + pad(str(self.direction), 2)
        result += ", Safety: " + str(self.safety)

        result += pad("[" + ", ".join(list(map(str, self.diff))), 35) + "]"

        result += ", Effective: " 
        result += pad("[" + ", ".join(list(map(str, self.effective_details))), 35) + "]"

        return result

    def getDiff(self):
        new_diff = []
        for i in range(1, len(self.details)):
            new_diff.append(self.details[i] - self.details[i-1])
        self.diff = new_diff.copy()

    def getDir(self):
        # Iterate over the diff and see which direction it tends
        inc = 0
        dec = 0

        for d in self.diff:
            if d > 0:
                inc += 1
            else:
                dec += 1

        if inc > dec:
            self.direction = 1
        else:
            self.direction = -1

    def getSafety(self, *debug):
        self.safety = 1 # how many mistakes can we make?
        details_backup = self.details.copy()
        k = 0

        if debug:
            print("Getting safety for " + str(self.details))
            print("Diff: " + str(self.diff))
            print("Dir: " + str(self.direction))
            print("------------")

        while k < len(self.details) - 1:
            if debug:
                print(str(self.details) + ", d" + str(self.diff))
                print("[" + str(k) + "]: " + str(self.details[k]))

            # Check if diff is within range
            if not (abs(self.diff[k]) >= 1 and abs(self.diff[k]) <= 3):
                if debug:
                    print("\tDiff at unsafe level!")
                    print("\t" + str(self.details))
                    print("\tDiff: " + str(self.diff))
                    print("\t[" + str(k) + "]: " + str(self.details[k]))
                
                self.safety -= 1
                if k == 0:
                    self.details.pop(k)
                else:
                    self.details.pop(k+1)
                self.getDiff()
                k = 0
                continue

            # Make sure all diffs are in the right direction
            if sign(self.diff[k]) != self.direction:
                if debug:
                    print("\tDiff not in same direction as report!")
                
                self.safety -= 1

                self.details.pop(k)
                # try delete k 
                # if it still broke then try delete k+1

                self.getDiff()
                k = 0
                continue

            k += 1
        
        self.effective_details = self.details.copy()
        self.details = details_backup.copy()
        self.getDiff()


reports_raw = open("test_input_02.txt", "r").readlines()
reports = []

for report_raw in reports_raw:
    if len(report_raw.strip()) > 0:
        reports.append(report(report_raw.strip()))
#reports.append(report(reports_raw[7]))

safe_reports = 0
i = 1

print("bingus\n")
for r in reports:
    #if r.dampened:
    print(pad(i, 4) + "/" + str(len(reports)) + " - " + str(r))

    # if r.safety < 0:
    #     print(pad(i, 4) + " - " + str(r))
    
    if r.safety >= 0:
        safe_reports += 1
    
    i += 1
    if i > 7:
        break

# 3

#test_report = report("1 3 2 4 5")
#test_report = report("55 53 54 56 57 58")
#print(test_report)
#test_report.details = test_report.details_backup.copy()
#test_unsafe = test_report.determineSafety()
#print(test_unsafe)

# Create report (1, 3, 2, 4, 5)
# Get diff (+2, -1, +2, +1)
# Count + and - 
# Remove odd one out (if 1)
# Get diff
# Count abs(value) < 1 | > 3
# Return true if <= 1

# problem when report is [9, 1, 2, 3, 4, 5]
# or [1, 2, 3, 4, 9, 6]

# Part 1: 432
# Part 2: 472 (too low) 460 (too low) 462 (wrong) 475 (wrong)
print("Total Safe Report: " + str(safe_reports))

# r = 13
# reports[r].getSafety(True)
# print(str(reports[r]))