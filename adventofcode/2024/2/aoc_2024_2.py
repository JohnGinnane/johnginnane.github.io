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

def determineSafety(levels):
    direction = 0

    if len(levels) == 0:
        return True

    if levels[0] < levels[-1]:
        direction = 1
    else:
        direction = -1

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
    details = []
    safe = False

    def __init__(self, data_str:str):
        self.details = list(map(int, data_str.split(" ")))        
        self.safety_count = 1
        self.safe = True

        if len(self.details) <= 0:
            return
        
        if (len(self.details) == 1) :
            return 
        
        # Iterate up from 0 to n with i
        # Check if details(0:i) is safe
        # If unsafe more than once then unsafe

        i = 1
        details_backup = self.details.copy()
        while i <= len(self.details):
            if determineSafety(self.details[0:i]):
                i += 1
            else:
                self.details.pop(i-1)
                self.safety_count -= 1

        self.details = details_backup.copy()

        if self.safety_count < 0:
            self.safe = False

        # what if we checked both sides of a level to see which 
        # number is best to delete?
        # 9 13 16 17 20


    def __str__(self):
        result = "Report: "
        if (self.safe):
            result += pad("SAFE", 9)
        else:
            result += pad("NOT SAFE", 9)

        result += " -> "
        result += pad("[" + ", ".join(list(map(str, self.details))), 40) + "]"

        result += " (safety: " + str(self.safety_count) + ")"

        return result

reports_raw = open("input_02.txt", "r").readlines()
reports = []

for report_raw in reports_raw:
    reports.append(report(report_raw))

safe_reports = 0
i = 1

for r in reports:
    #if r.dampened:
    #print(pad(i, 4) + "/" + str(len(reports)) + " - " + str(r))

    if r.safety_count <= 0:
        print(pad(i, 4) + " - " + str(r))
    
    if (r.safe):
        safe_reports += 1
    
    i += 1

# 3

#test_report = report("1 3 2 4 5")
#test_report = report("55 53 54 56 57 58")
#print(test_report)
#test_report.details = test_report.details_backup.copy()
#test_unsafe = test_report.determineSafety()
#print(test_unsafe)

# Part 1: 432
# Part 2: 472 (too low) 460 (too low) 462 (wrong) 475 (wrong)
print("Total Safe Report: " + str(safe_reports))