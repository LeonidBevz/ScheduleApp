import openpyxl


class EdPlan:
    plan = []
    planFloat = []
    sum = []

    def getPlanFromFile(self, path):
        if path[len(path) - 4:] != "xlsx":
            print("Incorrect file")
            return -1

        planbook = openpyxl.open(path, read_only=True)
        plansheet = planbook.worksheets[0]
        self.plan = []
        self.planFloat = []
        self.sum = []
        planstr = []
        i = 0
        for row in plansheet.iter_rows(min_row=29, max_row=35, min_col=2, max_col=104):
            planstr.append([])
            for cell in row:
                if cell.value != None:
                    planstr[i].append(str(cell.value))
            i += 1
        for i in range(len(planstr) - 1, 0, -1):
            if len(planstr[i]) < 2:
                planstr.pop(i)
        # print(planstr)
        if not (len(planstr) != 0 and len(planstr[0]) != 0 and "недел" in planstr[0][0]):
            print("Incorrect file")
            return -1

        for k in range(len(planstr)):
            self.plan.append([])
            self.planFloat.append([])
            for i in range(len(planstr[k])):
                planstr[k][i] = planstr[k][i].replace("\n", "")
                # print(planstr[k][i])
                strpart = ""
                floatpart = ""
                for j in range(len(planstr[k][i])):
                    if planstr[k][i][j] in "0123456789,":
                        floatpart += planstr[k][i][j]
                        if planstr[k][i][j + 1] not in "0123456789,":
                            break
                    else:
                        strpart += planstr[k][i][j]
                self.plan[k].append(strpart)
                floatpart = floatpart.replace(",", ".")
                self.planFloat[k].append(float(floatpart))
        for i in range(len(self.planFloat)):
            self.sum.append(0)
            for j in range(len(self.planFloat[i])):
                self.sum[i] += self.planFloat[i][j]

    def setPlan(self, names, nums, currCourse):
        if len(self.planFloat) == 0:
            self.planFloat.append([])
            self.plan.append([])
            self.sum.append([])
            currCourse = 0
        self.plan[currCourse] = []
        self.planFloat[currCourse] = []
        self.sum[currCourse] = 0
        for i in range(len(names)):
            self.plan[currCourse].append(names[i])
            self.planFloat[currCourse].append(nums[i])
            self.sum[currCourse] += nums[i]

