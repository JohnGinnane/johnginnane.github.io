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

def getDiff(list):
    new_diff = []
    for i in range(1, len(list)):
        new_diff.append(list[i] - list[i-1])
    return new_diff

def getDir(list):
    # Iterate over the diff and see which direction it tends
    inc = 0
    dec = 0

    for i in range(1, len(list)):
        if list[i] - list[i-1] > 0:
            inc += 1
        else:
            dec += 1

    if inc > dec:
        return 1
    else:
        return -1

def getIssues(list, *debug):
    issues = 0 # how many issues does this list have?
    dir = getDir(list)
    diff = getDiff(list)
    k = 0

    if debug:
        print("Getting safety for " + str(list))
        print("Diff: " + str(diff))
        print("Dir: " + str(dir))
        print("------------")

    while k < len(diff):
        if debug:
            print(str(list) + ", d" + str(diff))
            print("d[" + str(k) + "]: " + str(diff[k]))

        if sign(diff[k]) != dir:
            # Make sure all diffs are in the right direction
            if debug:
                print("\td[" + str(k) + "] does not align with direction!")
            issues += 1
        elif not (abs(diff[k]) >= 1 and abs(diff[k]) <= 3):
            # Check if diff is within range
            if debug:
                print("\td[" + str(k) + "] is outside safe limits!")
            issues += 1

        k += 1

    return issues

class report:
    effective_details = []
    details = []
    diff = []
    direction = 0
    safe_permutations = []
    safe = False

    def __init__(self, data_str:str):
        self.details = list(map(int, data_str.split(" ")))        
        self.safe = True
        self.direction = 0

        if len(self.details) <= 1:
            return

        self.safe_permutations = []

        # If the original report has issues then
        # iterate over each element and simulate
        # deleting it, then check issues again
        if getIssues(self.details) > 0:
            self.safe = False
            for i in range(0, len(self.details)):
                details_backup = self.details.copy()
                details_backup.pop(i)
                self.safe_permutations.append(getIssues(details_backup))

        # Find a permutation with 0 issues after we remove any element
        for i in range(0, len(self.safe_permutations)):
            if self.safe_permutations[i] == 0:
                self.safe = True
                break

    def __str__(self):
        result = "Report: "
        result += pad(str(self.details), 25) + ", Safe: " + pad(str(self.safe), 5) + ", Perm: " + str(self.safe_permutations)

        return result

reports_raw = open("input_02.txt", "r").readlines()
reports = []

for report_raw in reports_raw:
    if len(report_raw.strip()) > 0:
        reports.append(report(report_raw.strip()))

safe_reports = 0
i = 1

for r in reports:
    print(pad(i, 4) + "/" + str(len(reports)) + " - " + str(r))

    if r.safe == True:
        safe_reports += 1
    
    i += 1

# Part 1: 432
# Part 2: 488
print("Total Safe Report: " + str(safe_reports))