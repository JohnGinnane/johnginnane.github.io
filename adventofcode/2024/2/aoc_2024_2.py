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
        self.safe = True

        if len(self.details) <= 0:
            return
        
        last_num = self.details[0]
        direction = 0

        if (len(self.details) == 1) :
            return 
        
        for k in range(1, len(self.details)):
            v = self.details[k]
            diff = 0

            # First iteration direction is undetermined
            # So we check second element against first
            if direction == 0:
                if last_num < v:
                    direction = 1 # Levels are ascending
                else:
                    direction = -1 # Levels are descending
            
            diff = v - last_num
            last_num = v

            # Report is safe if all levels are increasing AND
            # the difference is at least 1 and at most 3
            if not(abs(diff) >= 1 and abs(diff) <= 3 and sign(diff) == sign(direction)):
                self.safe = False
                break

    def __str__(self):
        return "Report: [" + ", ".join(list(map(str, self.details))) + "]"

reports_raw = open("input_02.txt", "r").readlines()
reports = []

for report_raw in reports_raw:
    reports.append(report(report_raw))

safe_reports = 0
i = 1
for r in reports:
    print(pad(i, 4) + "/" + str(len(reports)) + " - " + str(r) + " -> Safe: " + str(r.safe))
    if (r.safe):
        safe_reports += 1
    i += 1

# 81
print("Total Safe Report: " + str(safe_reports))