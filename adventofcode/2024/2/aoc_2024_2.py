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

class report:
    details = []
    safe = False

    def __init__(self, data_str:str):
        self.details = list(map(int, data_str.split(" ")))
        self.details_backup = self.details.copy()
        self.safe = True
        self.dampened = False

        if len(self.details) <= 0:
            return
        
        if (len(self.details) == 1) :
            return 
        
        self.unsafe_indices = self.determineSafety()

        if len(self.unsafe_indices) == 1:
            self.details.pop(self.unsafe_indices[0])
            self.dampened = True
        elif len(self.unsafe_indices) > 1:
            self.safe = False

            #self.details.pop(self.unsafe_index)
            # unsafe_index = self.determineSafety()
            # self.safe = False

            # # Determined safe after dampened once
            # if unsafe_index < 0:
            #     self.safe = True
            #     self.dampened = True


    def __str__(self):
        result = "Report: "
        if (self.safe):
            result += pad("SAFE", 9)
        else:
            result += pad("NOT SAFE", 9)
        
        result += " -> ["
        result += ", ".join(list(map(str, self.details_backup)))
        result += "]"

        result += " ("
        result += self.getDiff()
        result += ")"

        # result += " ["
        # for i in range(0, len(self.details_backup)):
        #     result += str(self.details_backup[i])

        #     if i > 0:
        #         diff = self.details_backup[i] - self.details_backup[i-1]
        #         if diff > 0:
        #             result += " (+" + str(diff) + ")"
        #         else:
        #             result += " (" + str(diff) + ")"

        #     if i < len(self.details_backup) - 1:
        #         result += ", "
        # result += "]"

        if (self.dampened and self.safe):
            result += " (Dampened: ["
            result += ", ".join(list(map(str, self.details)))
            result += "])"

        return result
    
    def getDiff(self):
        result = ""
        for i in range(1, len(self.details_backup)):
            if result != "":
                result += ", "

            diff = self.details_backup[i] - self.details_backup[i-1]
            if diff > 0:
                result += "+"
        
            result += str(diff)
        return result

    def determineSafety(self):
        self.safe = True
        last_num = self.details[0]
        direction = 0
        unsafe_indices = []

        if self.details[0] < self.details[-1]:
            direction = 1
        else:
            direction = -1

        for k in range(1, len(self.details)):
            v = self.details[k]
            diff = v - last_num
            last_num = v

            # Report is safe if all levels are increasing AND
            # the difference is at least 1 and at most 3
            at_least = 1
            at_most = 3
            if not(abs(diff) >= at_least and abs(diff) <= at_most and sign(diff) == sign(direction)):
                self.safe = False
                unsafe_indices.append(k) # Unsafe index
        
        return unsafe_indices # All good :-)

reports_raw = open("input_02.txt", "r").readlines()
reports = []

for report_raw in reports_raw:
    reports.append(report(report_raw))

safe_reports = 0
i = 1

for r in reports:
    #if r.dampened:
    print(pad(i, 4) + "/" + str(len(reports)) + " - " + str(r))

    # if r.dampened or not r.safe:
    #     print(pad(i, 4) + " - " + str(r))
    
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